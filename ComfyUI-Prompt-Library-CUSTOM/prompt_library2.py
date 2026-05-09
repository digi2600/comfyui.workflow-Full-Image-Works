import json
import os
import uuid
import re
import random
from datetime import datetime
from aiohttp import web
from server import PromptServer

# Path to store the prompt library data
LIBRARY_FILE = os.path.join(os.path.dirname(__file__), "prompt_library_data.json")


def load_library():
    """Load the prompt library from disk."""
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"categories": [], "prompts": []}


def save_library(data):
    """Save the prompt library to disk."""
    with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def process_random_segments(text, rng=None):
    """
    Finds segments like {abc|xyz|123} and picks one choice randomly.
    Supports nested segments like {a|{b|c}}.
    Can use a provided random.Random instance for deterministic results.
    """
    if not text:
        return text

    if rng is None:
        rng = random

    def replace_choice(match):
        choices = match.group(1).split("|")
        return rng.choice(choices)

    # Regex: find anything inside { } that contains at least one |
    # and does NOT contain nested brackets. This ensures we process from inside out.
    pattern = r"\{([^{}]*\|[^{}]*)\}"
    
    # Process from the inside out until no more patterns match
    new_text = text
    while True:
        processed = re.sub(pattern, replace_choice, new_text)
        if processed == new_text:
            break
        new_text = processed
        
    return new_text


# ──────────────────────────────────────────────
#  REST API routes
# ──────────────────────────────────────────────
routes = PromptServer.instance.routes


@routes.get("/prompt_library/data")
async def get_library(request):
    return web.json_response(load_library())


@routes.post("/prompt_library/data")
async def save_library_route(request):
    data = await request.json()
    save_library(data)
    return web.json_response({"status": "ok"})


@routes.post("/prompt_library/category")
async def add_category(request):
    body = await request.json()
    library = load_library()
    category = {
        "id": str(uuid.uuid4()),
        "name": body["name"],
        "parent_id": body.get("parent_id"),
        "color": body.get("color", "#6366f1"),
        "created_at": datetime.now().isoformat(),
    }
    library["categories"].append(category)
    save_library(library)
    return web.json_response(category)


@routes.put("/prompt_library/category/{cat_id}")
async def update_category(request):
    cat_id = request.match_info["cat_id"]
    body = await request.json()
    library = load_library()
    for cat in library["categories"]:
        if cat["id"] == cat_id:
            cat.update({k: v for k, v in body.items() if k != "id"})
            break
    save_library(library)
    return web.json_response({"status": "ok"})


@routes.delete("/prompt_library/category/{cat_id}")
async def delete_category(request):
    cat_id = request.match_info["cat_id"]
    library = load_library()
    # Remove category and all sub-categories
    def get_all_ids(pid):
        ids = {pid}
        for c in library["categories"]:
            if c.get("parent_id") == pid:
                ids |= get_all_ids(c["id"])
        return ids

    ids_to_delete = get_all_ids(cat_id)
    library["categories"] = [c for c in library["categories"] if c["id"] not in ids_to_delete]
    library["prompts"] = [p for p in library["prompts"] if p.get("category_id") not in ids_to_delete]
    save_library(library)
    return web.json_response({"status": "ok"})


@routes.post("/prompt_library/prompt")
async def add_prompt(request):
    body = await request.json()
    library = load_library()
    prompt = {
        "id": str(uuid.uuid4()),
        "title": body["title"],
        "text": body["text"],
        "negative": body.get("negative", ""),
        "category_id": body.get("category_id"),
        "tags": body.get("tags", []),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    library["prompts"].append(prompt)
    save_library(library)
    return web.json_response(prompt)


@routes.put("/prompt_library/prompt/{prompt_id}")
async def update_prompt(request):
    prompt_id = request.match_info["prompt_id"]
    body = await request.json()
    library = load_library()
    for p in library["prompts"]:
        if p["id"] == prompt_id:
            p.update({k: v for k, v in body.items() if k != "id"})
            p["updated_at"] = datetime.now().isoformat()
            break
    save_library(library)
    return web.json_response({"status": "ok"})


@routes.delete("/prompt_library/prompt/{prompt_id}")
async def delete_prompt(request):
    prompt_id = request.match_info["prompt_id"]
    library = load_library()
    library["prompts"] = [p for p in library["prompts"] if p["id"] != prompt_id]
    save_library(library)
    return web.json_response({"status": "ok"})


# ──────────────────────────────────────────────
#  ComfyUI Node definition
# ──────────────────────────────────────────────
class PromptLibraryNode:
    """
    A node that lets you browse your saved prompt library
    and pipe a selected prompt into your workflow.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
				"prompts": ("STRING", {"default": ""}),
                "prompt_ids": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
            },
            "optional": {
                "prefix": ("STRING", {"default": "", "multiline": False}),
                "suffix": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "load_prompt"
    CATEGORY = "utils/prompts"
    OUTPUT_NODE = False

    def load_prompt(self, prompts="", prompt_ids="", seed=-1, prefix="", suffix=""):
        library = load_library()
        ids = [pid.strip() for pid in prompt_ids.split(",") if pid.strip()]
        matched = [p for p in library["prompts"] if p["id"] in ids]
        # Preserve the order from prompt_ids
        id_order = {pid: i for i, pid in enumerate(ids)}
        matched.sort(key=lambda p: id_order.get(p["id"], 0))

        texts = [p["text"].strip() for p in matched if p["text"].strip()]
        negatives = [p["negative"].strip() for p in matched if p.get("negative", "").strip()]

        positive = ", ".join(filter(None, [prefix.strip()] + texts + [suffix.strip()]))
        negative = ", ".join(negatives)

        # Apply randomization
        rng = random.Random(seed if seed != -1 else None)
        positive = process_random_segments(positive, rng)
        negative = process_random_segments(negative, rng)

        return (positive, negative)


class PromptLibraryRandomNode:
    """
    Picks a random prompt from one or more selected categories
    every time the workflow runs.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Comma-separated category IDs chosen in the UI
                "category_ids": ("STRING", {"default": ""}),
                # -1 = truly random each run, any other value = fixed seed
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
            },
            "optional": {
                "prefix": ("STRING", {"default": "", "multiline": False}),
                "suffix": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive", "negative", "prompt_title", "prompt_id")
    FUNCTION = "pick_random"
    CATEGORY = "utils/prompts"
    OUTPUT_NODE = False

    def pick_random(self, category_ids, seed=-1, prefix="", suffix=""):
        library = load_library()

        if not category_ids.strip():
            return ("", "", "", "")

        selected_ids = [cid.strip() for cid in category_ids.split(",") if cid.strip()]

        # Collect all descendant category ids
        def get_descendants(cid):
            ids = {cid}
            for c in library["categories"]:
                if c.get("parent_id") == cid:
                    ids |= get_descendants(c["id"])
            return ids

        all_cat_ids = set()
        for cid in selected_ids:
            all_cat_ids |= get_descendants(cid)

        pool = [p for p in library["prompts"] if p.get("category_id") in all_cat_ids]

        if not pool:
            return ("", "", "", "")

        rng = random.Random(seed if seed != -1 else None)
        chosen = rng.choice(pool)

        positive = " ".join(filter(None, [prefix.strip(), chosen["text"].strip(), suffix.strip()]))
        negative = chosen.get("negative", "")

        # Apply randomization using the same seed for reproducibility if seed != -1
        positive = process_random_segments(positive, rng)
        negative = process_random_segments(negative, rng)

        return (positive, negative, chosen.get("title", ""), chosen["id"])


class StringConcatenateNode:
    """
    A simple node that concatenates n string inputs.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "delimiter": ("STRING", {"default": ", "}),
                "input_count": ("INT", {"default": 2, "min": 2, "max": 20, "step": 1}),
            },
            "optional": {
                **{
                    f"string{i}": ("STRING", {"forceInput": True, "default": ""})
                    for i in range(1, 21)
                }
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Result",)
    FUNCTION = "concatenate"
    CATEGORY = "utils/strings"

    def concatenate(self, delimiter, input_count, **kwargs):
        values = []
        for i in range(1, input_count + 1):
            k = f"string{i}"
            if k in kwargs:
                values.append(str(kwargs[k]))
        return (delimiter.join(values),)

NODE_CLASS_MAPPINGS = {
    "PromptLibraryNode": PromptLibraryNode,
    "PromptLibraryRandomNode": PromptLibraryRandomNode,
    "StringConcatenateNode": StringConcatenateNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptLibraryNode": "📚 Prompt Library",
    "PromptLibraryRandomNode": "🎲 Prompt Library — Random",
    "StringConcatenateNode": "🔡 String Concatenate",
}

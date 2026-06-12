![Workflow Overview](Full%20Image%20Works%201.45.a.jpg)

Status & Disclaimer

This is an alpha/non-production release. All core functions work without critical errors, but I'm still refining several areas before considering it production-ready.
Current Limitations:

    Installation is complex (working on simplification)
    README documentation is ~80% complete (a few sections remain)
    Some sections need refinement (see Known Issues below)
    Open to modifications and improvements that enhance usability or installation

Known Issues

    Inpaint and Restore Image sections — Need refinement for better reliability
    Step 2 modules — Some still in development (Skin Fix module particularly)
    Model focus — Primarily designed for SDXL-type models, with a small Flux section included

Requirements

    ComfyUI
    19 custom nodes (see list at bottom of README)
    Tested on AMD 16GB VRAM; should work on any card capable of generating SDXL 1.0 images

<br>    
   I have created a very large and, I think, very unique workflow that is very advanced, but I am afraid it is advanced in some areas and missing some of the more basic parts. I have been making it by trial and error as I go along, and have made it really flexible. Most of the options have been designed with SDXL models in mind, but there are a few exceptions with FLUX, Inpaint, and Kandinsky5.<br>
  
To give an example, I generally use:
<ul>
   <li>The SDXL based 'cyberrealisticPony_v141.safetensors' 
      <ul>
      <li>A larger, but also faster and less Vram consuming model. While it is not strictly known for being 'photorealistic', it is generally 'good enough'. 
         <li>Used best with Danbooru tags (1girl, solo, etc.).</li></ul>
   <li>The SDXL based  'juggernautXL_ragnarokBy.safetensors'
      <ul>
   <li>Known for being more 'photorealistic', this is a slightly slower and more Vram hungry model. It is also harder to control and might give better results than my favored pony model sometimes,  and terrible results most other times.
      <li>Used best with Natural Language prompts (A woman standing...)</li>
      </ul>
</li>
</ul><br>

   There are two main sections or Steps. First is the input step. A long side of the workflow with dynamic choices for text-to-image, image-based + text-to-image, inpainting, photo restoration, flux-only, and a few more. The second step is the fine-tuning part. Again, fully dynamic, where you can pick and/or all of the "modules" like skin fix, face fix, K-Sampler Cycle fix, face swap, upscale, and more.

   Some parts have been added and adapted from other sources on the internet. An example is the flux image generation part. I did not make that one, but I did use other nodes to incorporate it into the workflow as another generation option within the list of "step 1" generation choices.

   There are options within options here that are constantly being rewritten, streamlined, and even a few unfinished (but hopefully working) parts. I'll try to keep this as short as possible while hopefully explaining a good amount.

   I have created this using a Windows box with an AMD 16GB VRAM card. It has taken me months to find the perfect balance of torch/Rocm/nodes/onnx/drivers and more. It might be a great idea to update in most cases, but this has taken me months, and I have no wish to update all and risk having to delete everything and re-install (I’m especially looking at you, ReActor. A great little node, but picky as hell)… Due to possible health and family concerns, I am trying to add this to a public repo asap and have not written everything down yet. This will take a number of custom nodes that I think some people will have problems with, and it might not be the most efficient, but it is working for me, and I have only been using ComfyUI image generation for about 10 months now, and I have never really gone over the basic steps. I just learned today that the ComfyUI Manager has a snapshot manager…damn. That could have saved me about a month of work alone.

> [!IMPORTANT]
> ❗️Each section in steps 1 and 2 will have a ‘Preview Image’ box. The workflow does not use any auto-save method. Please only right-click and choose Save As in the ‘Preview Image’ box (this is fine with batch images as well). Saving from the ‘Image Comparer’ or anything else might not work or give unexpected results. The only exception is the video module at the very end, that does save a file after each run.



<h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Step 1:</h1><br>
First, start by selecting one of several different ways to start within the "Step 1" section 'Choose' box.<br>

![Workflow Start](choose1.jpg)

<br>
&nbsp;&nbsp;&nbsp;&nbsp;👉 Generate Image from Text.<br> This is the most used and robust option. Just type what you want to see in the positive prompt and type what you don't want to see in the negative. Sound easy? Ha! By default, it will create a batch of 4 images.<details>
    <ul>
        I am trying to go in some top-down, left-to-right logical order.
        <li>First is a notes box.</li>
        <li>The "Set" box where you can choose several options</li>
        <ul>
            <li>ckpt_name - The model name you are using. This is normally a checkpoint file, like cyberrealisticPony_v141.safetensors or sd-v1-5.safetensors</li>
            <li>steps</li> 
            <li>cfg</li>
            <li>sampler_name</li>
            <li>scheduler</li>
            <li>denoise</li>
            <li>resolution</li>
            <li>batch_size</li>
            <li>stop_at_clip_layer -  option to control clip encoding for lesser or greater detail/control.</li>
            <li>Low Vram - A toggleable setting enabling titled VAE for easier Vram use and Vram debugging and clearing to increase speed and efficiency.</li>
        </ul>
         <li>The rgthree seed selector node makes seed control much easier and faster.</li>
        <li>The power lora loader by rgthree to load any lora's you wish.</li>
        <li>Prompt Library - This will enable you to choose a prompt by building it with a set of pre-made cards allowing you a starting pad to try new combinations.</li>
        <li>The 'Prompt Library 2 Auto Positive Prompt' and 'Prompt Library 2 Auto Negative Prompt' are where the selected prompt is displayed.</li>
        <li>The two boxes under that are the 'Additional Positive Prompt' positive prompt (Green as well) and 'Additional Negative Prompt' in red color, to enable a quick addition of any extra or typed prompts. This can be used in addition to the first positive prompt, the only positive prompt, or just left blank. It's all dynamic.</li>
        <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.</li>
        <li>The ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to send to "step 2"-image adjustment.</li>
        <li>The last two boxes represent the combined output of the auto prompt and the manual prompt, placed into the combined positive and negative prompts for added convenience.</li>
</ul></details><br>
  
&nbsp;&nbsp;&nbsp;&nbsp;👉 Generate Image from Image and Text.<br> By default, it will create a batch of 4 images.<details>
    <ul>
  <li>You have the "set" box where you can choose:
    <ul>
      <li>the checkpoint, steps, cfg, and other normal settings, including the width and height. (Remember to mess with denoise to give the generating model more or less freedom in the new image!)
      <li>batch size should stay at 4, but I think 2 is doable, but not very tested.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>stop_at_clip_layer option to control clip encoding for lesser or greater detail/control.
      <li>✏️Vram debugging and clearing to increase speed and efficiency.</li>
    </ul>
   <li>The power lora loader by rgthree to load any lora's you wish.
   <li>The rgthree seed selector node makes seed control much easier and faster.
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>Image Comparer (rgthree) allows you to compare each image in the batch to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   <li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to send to "step 2"-image adjustment.
  </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Inpaint.<br> Can be tricky. The end of the section has a second model selected to go off a non-Inpaint model.<br>
❗️This input step is currently not working well. I am leaving it in hopes that it can be fixed at a later date.<details>
<ul>
  <li>There are two ‘Load Image’ boxes. Load the same image into both of these, then right-click the lower one and select ‘Open in Maskeditor’ to highlight the section of the image that you want to change.
  <li>The Set box will have many options you can change, like the model, vae_name, clip layer, and so on.
    <ul>
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>stop_at_clip_layer option to control clip encoding for lesser or greater detail/control.
      <li>✏️Vram debugging and clearing to increase speed and efficiency.</li>
    </ul>
  <li>The rgthree seed selector node makes seed control much easier and faster.
  <li>The power lora loader by rgthree to load any lora's you wish.
  <li>Main positive prompt (Green) and Negative prompt (Red).
  <li>A ‘Mask Preview’ box that just shows what it is working with for clarity.
  <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
  <li>Another load checkpoint box so you can continue to step 2 with a full (not inpaint only) model. 
    <ul>
       <li>Note: Most modules in Step 2 have been updated to where you must select a safe tensors file when needed, so this might not be used in most cases. This is a great way of mixing the different model parts together, like the face fix. I normally use Pony and Juggernaut, and now have the option to generate an image with Pony, but I experiment with some fixes with other models to only fix the Fine tune Image, skin, face, or hands. </li></ul>
  <li>The preview image box should show the image generated, and is always the best way to save any image you choose.
  </li>
</ul></details><br>


&nbsp;&nbsp;&nbsp;&nbsp;👉 Flux. <br>Use text-to-image generation with Fulx.<details>
<ul>
<li>The Set box will have many options you can change, like the model (unet), clip names, and so on.
    <ul>
      <li>batch size should stay at 2.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>✏️Vram debugging and clearing to increase speed and efficiency.</li>
    </ul>
<li>The rgthree seed selector node makes seed control much easier and faster.
<li>Main positive prompt (Green).
<li>The preview image box should show the image generated, and is always the best way to save any image you choose.
<li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to send to "step 2"-image adjustment.
   </li>
</ul></details><br>


&nbsp;&nbsp;&nbsp;&nbsp;👉 Image to text<br> Uses 'comfyui-easy-use/easy imageInterrogator' node to read images into text descriptions. See how an AI describes images. You can also take the description and copy it to the 'Generate Image from Text' to change it anyway you want.<details>
<ul>
   <li>Load Image box for any image you want the AI to 'see'.
  <li>The Set box will have many options you can change, like the model, steps, cfg, and so on.
    <ul>
      <li>batch size should stay at 4, but I think 2 is doable, but not very tested.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>'Generate Image' will take the text output and re-generate using only the text created, in batches, to compare it's description from the main image to a copy to visually see the differences.
      <li>✏️Vram debugging and clearing to increase speed and efficiency. </li>
    </ul>
   <li>The rgthree seed selector node makes seed control much easier and faster.
   <li>The Positive and negative prompts are actually just text as output from the imageInterrogator node, and can't be directly edited.
   <li>The preview image box should show the image generated, and is always the best way to save any image you choose.
   <li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to send to "step 2"-image adjustment.
   </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Florence2 image to text<br> Another type of image-to-text node that usually gives better or more detailed results. <br>
❗️Due to it needing a different model in order to first read the image, there are two sections in the 'Florence2 image to text' box.<details>
<ul>
   <li>Load Image box for any image you want the AI to 'see'. 
  <li>The Set box will have many options you can change, like the model, steps, cfg, and so on. Any options above the 'Generate Image?' option in the box is for the Florence2 model. Any option under 'Generate Image?' is for generating a new image using the output.
    <ul>
      <li>'Generate Image' will take the text output and re-generate using only the text created, in batches, to compare it's description from the main image to a copy to visually see the differences.
       <li>batch size should stay at 4, but I think 2 is doable, but not very tested.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>✏️Vram debugging and clearing to increase speed and efficiency. </li>
    </ul>
   <li>The rgthree seed selector node makes seed control much easier and faster.
   <li>The Positive and negative prompts are actually just text output from the imageInterrogator node and can't be directly edited.
   <li>The preview image box should show the image generated, and is always the best way to save any image you choose.
   <li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to send to "step 2"-image adjustment.   
   </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Restore Image<br>
Simple image restoration. The checkpoint selection for a model does nothing to the 'Restore Image' section and is only used in some areas of Step 2.<details>
<ul>
   <li>Load Image box for any image you want to restore. 
   <li>The Set box will have many options you can change for image restoration.
   <li>The Positive and negative prompts are actually just text as output from the imageInterrogator node, and can't be directly edited.
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show the image generated, and it is always the best way to save any image you choose.
   </li>
</ul></details><br>

> [!NOTE]
> ✏️Note: Press the number 1 to jump back to the 'Step 1 Choice box' area.

<br><br><br>





<h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Step 2:</h1><br>
You can choose to enable any option, or options, to continue. This was added to make it easier to generate several times until you get a result you want to work with. Just click any yes or no button(s) in the ‘Choose’ menu at step 2. All modules are fully modular and made to work in any combination or number, but they can not change the direction (i.e., no Upscale before Face Swap. Only Face Swap and then Upscale.) So you can use the Face Fix and the Upscale while leaving Fine Tune, Face Swap, and Blend and Adjust Face Expression disabled, and it should just skip them. But I suggest only activating extra groups one at a time (You don't have to process more until you are ready, otherwise it will be a lot of wasted generations and slow things down. A good example is if I wanted to do Face Fix and Upscale, I would first do Face Fix, then come back to this menu (press '2' to jump here) and then enable Upscale, leaving Face Fix still on.)<br><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Fine Tune Image<br>
Will take the one image you selected from the previous batch of pictures and give it a re-touch. A light re-draw to the full image to help with artifacts or changes. This will give you a new batch of 4 images (same "Batch image" and shows "Image #" as above).<details>
<ul>
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>You have the "set" box where you can choose :
    <ul>
      <li>the checkpoint, steps, cfg, and other normal settings. (Remember to mess with denoise to give the  generating model more or less freedom in the new image!)
      <li>’Number of Images’ is the number of images to generate in a batch. 4 is the best as I have found.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>stop_at_clip_layer option to control clip encoding for less or greater detail/control.
      <li>✏️Vram debugging and clearing to increase speed and efficiency.</li>
    </ul>
   <li>The rgthree seed selector node makes seed control much easier and faster.
   <li>The power lora loader by rgthree to load any lora's you wish.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   <li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to another module, like upscale.
   </li>
</ul></details><br>


&nbsp;&nbsp;&nbsp;&nbsp;👉 Skin Fix<br>
It is usually best to do this step before a Face or Hand Fix; however, I normally do not use this very often, as the results are usually bad, and you might spend a long time messing with the settings.<details>
<ul>
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>You have the "set" box where you can choose several options.
   <li>The power lora loader by rgthree to load any lora's you wish.
   <li>The SkinDetailer box.
   <li>The pink masking box with three different windows that show which mask in chosen and how it is selected.
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Face Fix<br>
Regenerate a new face. Many faces you generate will have bad faces, like crooked eyes, or something wrong, but the body is perfect. This will help if you used too many loras and messed up the face.<details>
<ul>
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>You have the "set" box where you can choose several options.
   <li>The power lora loader by rgthree to load any lora's you wish.
   <li>The FaceDetailer box.
   <li>The pink masking box with three different windows that show which mask in chosen and how it is selected.
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Hand Fix<br>
This will try to find and fix broken or messed-up fingers and hands.<details>
<ul>
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>Three small boxes under the prompt windows with detailer options.
   <li>The FaceDetailer box (with hand_* in UltralyticsDetectorProvider).
   <li>The pink masking box with three different windows that show which mask in chosen and how it is selected.
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Ksampler Cycle Fix<br>
Much like 'Fine Tune Image', this will redraw the image using cycles of the sampler and combine them. This is more focused on blending and refining any 'Fix', but can be used alone, without any other 'Fix' enabled.<details>
<ul>
   <li> test </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Face Swap<br>
Use face swap to change the face on the image to another face. ReActor is a fast and good faceswap, just very hard to install, at least is was very difficult for me!<details>
<ul>
   <li>First is the ReActor Fast Face Swap box. 
    <ul>
      <li>✏️The only real setting you will want to change is the 'input_faces_index' to search for faces (starting from left to right, 0,1, etc.) So if you only want to change the second person's face in a photo, you would just put 1. It can take some playing with before it finds the right thing. Remember that anything that is close to a face counts! Posters, people way in the background, the Monalisa, a pile of garbage that kinda looks like a face if you squint really hard.</li>
    </ul>
   <li>Swap Choice box. A choice of auto-selecting up to 3 extra faces. This was put in to make it easier if you don't want to mess with the index count.
   <li>ReActor Face Booster. You can try using this, or disable it. The booster is usually a little much and can make things look odd.
   <li>Load Image box for any image you want to work on. 
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Face Swap (SimSwap)<br>
A different version of Face Swap is used. SimSwap is a higher-quality and more adjustable tool, but it is also very hard to get right.<details>
<ul>
   <li> test </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Blend and Adjust Face Expression<br>
Change the lighting, contrast, and other image settings with the ability to change some facial parameters.<details>
<ul>
   <li> test </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Upscale<br>
1x and 2x Upscale with a second preview window showing the 1x upscale version without the enlargement at full 1 to 1 quality. Upscales will have some light image enhancement and fine detail added(like hair, face, etc.).<details>
<ul>
   <li> test </li>
</ul></details><br>

&nbsp;&nbsp;&nbsp;&nbsp;👉 Video<br>
A small workflow that I added and changed a few things to make it where I  could dynamically just add the image I made through the workflow (it just saves me the time of saving files and swapping workflows)<details>
<ul>
   <li> test </li>
</ul></details><br>


Would I ever do Face Fix and Face Swap at once? Well, yes. I have had several face swaps that looked odd because the face finder didn't work well and gave her a crooked jaw or no real lower lip...so A fresh regen of the face might help.<br>
Remember: Face Fix (Or regen) will capture ANY face (Picture on a shirt, poster, background guy, anything. But the Face Swap only works on one face unless you mess with the input_faces_index, and there is no way to get the Expressions node to work with more than one face, so you might find it useful to do a face regen on a photo of two hikers when they find a bear. Use Face Fix to tweak the facial features just about right, then do a face swap, and the face swap should overlay the face on top, not overwrite it. But just in case...now you can. Yay!<br>
<br>
> [!NOTE]
> ✏️Note: Press the number 2 to jump back to the 'step 2 Choice(s) box' to enable different things!)

<br><br>
Change log

1.45a (6/12/26)
<ul>
<li>Removed the `Quick Image` section in Step 1 options.</li>
<li>Improved and deployed Vram subgraph to each section and module.</li>
<li>Added several new sections to 'Generate Image from Text' box, including the custom Prompt Library node I have made. You can choose any prompt by clicking; this will affect both positive and negative prompting when changed. This will be built into a text string that will be shown under the node window, in green (for positive prompts) and red (for negative prompts). Two boxes are provided below them, both colored Green and red like the prompt boxes, allowing you to type anything to be added to the generator. </li>
<li>Added two windows at the end of the 'Generate Image from Text' box that give you a quick output of both the auto-prompt created by Prompt Library 2 and manual entry to easily copy and paste if needed.</li>
<li>Added two new modules to Step 2 area. '02) Auto select inpaint with Florence2' and '03) Selectable inpaint with SEGS'.</li>
<li>Added four new options in '10) Blend and Adjust Face Expression'. PencilSketch, FilmGrain, Quantize, and Solarize can be used individually or combined for different effects.</li>
<li>Skin Fix, Face Fix now has a dedicated checkpoint loader. Hand Fix still uses the original model.</li>
<li>Ksampler Cycle Fix now has a 'Custom' toggle button to use in place of the original model/clip/prompts</li>
</ul><br>
    
    
1.44.5-alpha-2 (5/1/26)
<ul>
<li>All Step 1 image generation options now use tiled VAE decode for efficient VRAM usage (with full VAE decode fallback available)</li>
<li>VRAM debugging via comfyui-kjnodes for better memory management</li>
<li>Batch Image selectors now use 1-based numbering (select image #1 for the first image, not #0)</li>
<li>New Step 1 section called 'Quick Image' with node from https://github.com/florestefano1975/ComfyUI-Prompt-Library. I am hoping to replace the Prompt database used in 'Generate Image from Text' with a more flexible one.</li>
<li>Added the Vram selector box to "5) Ksampler Cycle Fix" with both the option to use free VAE or tiled, and Vram Debug</li>
<li>Added 'PC: Schedule LoRAs' to Step 1 section called 'Quick Image' from https://github.com/asagi4/comfyui-prompt-control to enable LoRA adding within the prompt <lora:filename:1.0></li>
<li>Cleaned up some extra nodes (preview image nodes and one Context (rgthree)node)</li>
</ul><br>
    
******************************************
<ul>
<li>Python version: 3.11.9</li>
<li>AMD arch: gfx1201</li>
<li>ROCm version: (7, 2)</li>
<li>ComfyUI version: 0.20.1</li>
<li>ComfyUI frontend version: 1.42.15</li>
<li>Torch version: 2.10.0+rocm7.12.0a20260201</li>
</ul><br>
19 custom nodes:<details>
   <ul>
   <li>ComfyUI-Prompt-Library from https://github.com/NoudH/ComfyUI-Prompt-Library (Please use the custom copy in the files section above)</li>
<li>ComfyUI Impact Pack 8.28.2</li>
<li>ComfyUI-Custom-Scripts 1.2.5</li>
<li>rgthree-comfy 1.0.251211205</li>
<li>ComfyUI-AdvancedLivePortrait 1.0.0</li>
<li>ComfyUI-KJNodes 1.2.9</li>
<li>ComfyUI-Easy-Use 1.3.4</li>
<li>ComfyUI-Florence2 1.0.8</li>
<li>ComfyUI_UltimateSDUpscale 1.7.2</li>
<li>ComfyUI-ReActor 0.7.0-a1</li>
<li>ComfyUI_essentials 1.1.0</li>
<li>ComfyUI-Inpaint-CropAndStitch 3.0.7</li>
<li>ComfyUI Impact Subpack 1.3.5</li>
<li>ComfyUI-post-processing-nodes 1.0.1</li>
<li>WAS Node Suite (Revised) 3.0.1</li>
<li>lora-info 1.0.2</li>
<li>ComfyUI-Basic data handling 1.5.0</li>
<li>comfyui-simswap nightly</li>
    <li>ComfyUI-RvTools_v2 2.5.1</li>

   </ul>
</details>

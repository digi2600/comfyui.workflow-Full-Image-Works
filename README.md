I have created a very large and, I think very unique workflow that is very advanced, but I am afraid it is advanced in some areas and missing some of the more basic parts. I have been making it by trial and error as I go along, and have made it really flexible. 

There are two main sections or Steps. First is the input step. A long side of the workflow with dynamic choices for text-to-image, image-based + text-to-image, inpainting, photo restoration, flux-only, and a few more. The second step is the fine-tuning part. Again, fully dynamic, where you can pick and/or all of the "modules" like skin fix, face fix, K-Sampler Cycle fix, face swap, upscale, and more.

Some parts have been added and adapted from other sources on the internet. An example is the flux image generation part. I did not make that one, but I did use other nodes to incorporate it into the workflow as another generation option within the list of "step 1" generation choices.

There are options within options here that are constantly being rewritten, streamlined, and even a few unfinished (but hopefully working) parts. I'll try to keep this as short as possible while hopefully explaining a good amount.

I have created this using a Windows box with an AMD 16GB VRAM card. It has taken me months to find the perfect balance of torch/Rocm/nodes/onnx/drivers and more. It might be a great idea to update in most cases, but this has taken me months, and I have no wish to update all and risk having to delete everything and re-install (I’m especially looking at you, ReActor. A great little node, but picky as hell)… Due to possible health and family concerns, I am trying to add this to a public repo asap and have not written everything down yet. This will take a number of custom nodes that I think some people will have problems with, and it might not be the most efficient, but it is working for me, and I have only been using ComfyUI image generation for about 10 months now, and I have never really gone over the basic steps. I just learned today that the ComfyUI Manager has a snapshot manager…damn. That could have saved me about a month of work alone.

❗️Each section in steps 1 and 2 will have a ‘Preview Image’ box. The workflow does not use any auto-save method. Please only right-click and choose Save As in the ‘Preview Image’ box (this is fine with batch images as well). Saving from the ‘Image Comparer’ or anything else might not work or give unexpected results. The only exception is the video module at the very end, that does save a file after each run.



Step 1:
First, start by selecting one of several different ways to start within the "Step 1" section 'Choose' box.
👉Generate Image from Text. By default, it will create a batch of 4 images.
  ⇒You have the "set" box where you can choose :
    →the checkpoint, steps, cfg, and other normal settings, including the width and height. 
    →batch size should stay at 4, but I think 2 is doable, but not very tested.
    →Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
    →stop_at_clip_layer option to control clip encoding for lesser or greater detail/control.
    ✏️Vram debugging and clearing to increase speed and efficiency.
  ⇒The power lora loader by rgthree to load any lora's you wish.
  ⇒The rgthree seed selector node makes seed control much easier and faster.
  ⇒Main positive prompt (Green) and Negative prompt (Red).
  ⇒2nd positive prompt (Green as well) using Prompt database from benstaniford/comfy-prompt-db, to enable a quick selection of normally used prompts. This can be used in addition to the first positive prompt, the only positive prompt, or just left blank. It's all dynamic.
  ⇒The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
⇒And the ‘Batch Image’ box, where you can select the image you want to use in Step 2.
✏️Notice the text within the ‘Batch Image’ box shows ‘Image #’, this is an updated number scheme where the first image is 1, then 2, and so on. 
❗️Once you generate a good image that you like, select the little box next to the end that says "Batch image" and shows "Image #" as this will send only the image from the batch that you like to "step 2"-image adjustment.
  
👉Generate Image from Image and Text. By default, it will create a batch of 4 images. 
⇒You have the "set" box where you can choose :
   →the checkpoint, steps, cfg, and other normal settings, including the width and height. (Remember to mess with denoise to give the  generating model more or less freedom in the new image!)
   →fit should be ‘contain’ in most cases.
   →amount is the amount in batch to generate. 4 is the best as I have found.
⇒The power lora loader by rgthree to load any lora's you wish.
⇒The rgthree seed selector node makes seed control much easier and faster.
⇒Main positive prompt (Green) and Negative prompt (Red).
⇒Image Comparer (rgthree) allowing you to compare each image in the batch to the original image.
⇒The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
❗️ While this has the same looking “Batch Image” select box at the end of the section like above, it is not updated to the same number scheme yet. For image 1, select 0. For image 2 select 1, and so on.
✏️ This only uses the more efficient tile VAE decode
✏️ When the ‘Batch Image’ box shows ‘batch_index’, this does not use the same number scheme, and you must choose 0 for the first image, 1 for the 2nd image, and so on.



👉Inpaint. Can be tricky. The end of the section has a second model selected to go off a non-Inpaint model.
⇒There are two ‘Load Image’ boxes. Load the same image into both of these, then right-click the lower one and select ‘Open in Maskeditor’ to highlight the section of the image that you want to inpaint.
⇒The Set box will have many options you can change, like the model, vae_name, clip layer, and so on.  ⇒The rgthree seed selector node makes seed control much easier and faster.
⇒The power lora loader by rgthree to load any lora's you wish.
⇒Main positive prompt (Green) and Negative prompt (Red).
⇒A ‘Mask Preview’ box that just shows what it is working with for clarity.
⇒Image Comparer (rgthree) allowing you to compare the generated image to the original image.
⇒Another load checkpoint box so you can continue to step 2 with a full (not inpaint only) model. 
Note: Most modules in Step 2, have been updated to where you must select a safetensors file when needed, so this might not be used. This is a great way of mixing the different model parts together, like the face fix. I normally use Pony and Jaggernaut, and now have the option to generate an image with Pony, but I experiment with some fixes with other models to only fix the Fine tune Image, skin, face, or hands.
⇒The preview image box should show the image generated, and is always the best way to save any image you choose.

✏️ This only uses the more efficient tile VAE decode



👉Flux. Use text to image generation with Fulx.
⇒The Set box will have many options you can change, like the model (unet), clip names, and so on.  
⇒The ‘Vram setting’ box allows you to select Normal Vram use (high memory) or Low Vram (Tiled). Please make sure only one is selected.
⇒The rgthree seed selector node makes seed control much easier and faster.
⇒Main positive prompt (Green).
⇒The preview image box should show the image generated, and is always the best way to save any image you choose.
⇒And the ‘Batch Image’ box, where you can select the image you want to use in Step 2.
✏️ When the ‘Batch Image’ box shows ‘batch_index’, this does not use the same number scheme, and you must choose 0 for the first image, 1 for the 2nd image, and so on.




👉Image to text. Reads images into text descriptions. See how an AI describes images. You can also take the description and copy it to the 'Generate Image from Text' to change it any way you want.

👉Florance2 image to text. Another type of image to text nodes that usually gives better or more detailed results.

👉Restore Image

(Note: Press the number 1 to jump back to step 1, ‘Choose’ box area.)






Step 2:
You can choose to enable any option, or options, to continue. This was added to make it easier to generate several times until you get a result you want to work with. Just click any yes or no button(s) in the ‘Choose’ menu at step 2. All modules are fully modular and made to work in any combination or number, but they can not change the direction (i.e., no Upscale before Face Swap. Only Face Swap and then Upscale.) So you can use the Face Fix and the Upscale while leaving Fine Tune, Face Swap, and Blend and Adjust Face Expression disabled, and it should just skip them. But I suggest only activating extra groups one at a time (You don't have to process more until you are ready, otherwise it will be a lot of wasted generations and slow things down. A good example is if I wanted to do Face Fix and Upscale, I would first do Face Fix, then come back to this menu (press '2' to jump here) and then enable Upscale, leaving Face Fix still on.)

👉Fine Tune Image
Will take the one image you selected from the previous batch of pictures and give it a re-touch. A light re-draw to the full image to help with artifacts or changes. This will give you a new batch of 4 images (same "Batch image" and shows "Image #" as above).
⇒Main positive prompt (Green) and Negative prompt (Red).
⇒You have the "set" box where you can choose :
   →the checkpoint, steps, cfg, and other normal settings. (Remember to mess with denoise to give the  generating model more or less freedom in the new image!)
   →’Number of Images’ is the number of images to generate in a batch. 4 is the best as I have found.
⇒The rgthree seed selector node makes seed control much easier and faster.
⇒The power lora loader by rgthree to load any lora's you wish.
⇒The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
⇒The ‘Batch Image’ box, where you can select the image you want to move to another section, like upscale.

❗️Once you generate a good image that you like, select the little box next to the end that says "Batch image" and shows "Image #" as this will send only the image from the batch that you like to the next selection.
✏️ This only uses the more efficient tile VAE decode
✏️Notice the text within the ‘Batch Image’ box shows ‘Image #’, this is an updated number scheme where the first image is 1, then 2, and so on. 



👉Skin Fix
It is usually best to do this step before a Face or Hand Fix. Remember: Each 'Fix' has positive and negative prompts for each section.

👉Face Fix
Regenerate a new face. Many faces you generate will have bad faces, like crooked eyes, or something wrong, but the body is perfect. This will help if you used too many loras and messed up the face.

👉Hand Fix
This will try to find and fix broken or messed-up fingers and hands.

👉Ksampler Cycle Fix
Much like 'Fine Tune Image', this will redraw the image using cycles of the sampler and combine them. This is more focused on blending and refining any 'Fix', but can be used alone, without any other 'Fix' enabled.

👉Face Swap
Use face swap to change the face on the image to another face. (Up to four different face swaps per image!)

👉Face Swap (SimSwap)
A different version of Face Swap is used. SimSwap is a higher-quality and more adjustable tool, but it is also very hard to get right.

👉Blend and Adjust Face Expression
Change the lighting, contrast, and other image settings with the ability to change some facial parameters.
 
👉Upscale
1x and 2x Upscale with a second preview window showing the 1x upscale version without the enlargement at full 1 to 1 quality. Upscales will have some light image enhancement and fine detail added(like hair, face, etc.).

👉Test video creation node



Would I ever do Face Fix and Face Swap at once? Well, yes. I have had several face swaps that looked odd because the face finder didn't work well and gave her a crooked jaw or no real lower lip...so A fresh regen of the face might help.
Remember: Face Fix (Or regen) will capture ANY face (Picture on a shirt, poster, background guy, anything. But the Face Swap only works on one face unless you mess with the input_faces_index, and there is no way to get the Expressions node to work with more than one face, so you might find it useful to do a face regen on a photo of two hikers when they find a bear. Use Face Fix to tweak the facial features just about right, then do a face swap, and the face swap should overlay the face on top, not overwrite it. But just in case...now you can. Yay!

(Note: Press the number 2 to jump back to step 2 ‘Choose’ box to enable different things!)

******************************************

Python version: 3.11.9
AMD arch: gfx1201
ROCm version: (7, 2)
ComfyUI version: 0.11.1
ComfyUI frontend version: 1.37.11
Torch version: 2.10.0+rocm7.12.0a20260201

18 custom nodes:
ComfyUI Impact Pack 8.28.2
ComfyUI-Custom-Scripts 1.2.5
rgthree-comfy 1.0.251211205
ComfyUI-AdvancedLivePortrait 1.0.0
ComfyUI-KJNodes 1.2.9
ComfyUI-Easy-Use 1.3.4
ComfyUI-Florence2 1.0.8
ComfyUI_UltimateSDUpscale 1.7.2
ComfyUI-ReActor 0.7.0-a1
ComfyUI_essentials 1.1.0
ComfyUI-Inpaint-CropAndStitch 3.0.7
ComfyUI Impact Subpack 1.3.5
ComfyUI-post-processing-nodes 1.0.1
WAS Node Suite (Revised) 3.0.1
lora-info 1.0.2
ComfyUI-Notifications nightly
comfyui-simswap nightly
Prompt Database for ComfyUI unknown

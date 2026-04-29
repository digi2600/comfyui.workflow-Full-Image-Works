![Workflow Overview](Full%20Image%20Works%201.44.5.jpg)
   I have created a very large and, I think, very unique workflow that is very advanced, but I am afraid it is advanced in some areas and missing some of the more basic parts. I have been making it by trial and error as I go along, and have made it really flexible. Most of the options have been designed with SDXL models in mind, but there are a few exceptions with FLUX, Inpaint, and Kandinsky5.<br>
To give an example, I generally use:
<ul>
   <li>The SDXL based 'cyberrealisticPony_v141.safetensors' 
      <ul>
      <li>A larger, but also faster and less Vram consuming model. While it is not strictly known for being 'photorealistic', it is generally 'good enough'. 
         <li>Used best with Danbooru tags (1girl, solo, etc.).</li></ul>
   <li>The SDXL based  'juggernautXL_ragnarokBy.safetensors'
      <ul>
   <li>Known for being more 'photorealistic', this is a slightly slower, and more Vram hungry model. It is also harder to control and might give better results than my favored pony model sometimes,  and terrible results most other times.
      <li>Used best with Natural Language prompts (A woman standing...)</li>
      </ul>
</li>
</ul><br>

   There are two main sections or Steps. First is the input step. A long side of the workflow with dynamic choices for text-to-image, image-based + text-to-image, inpainting, photo restoration, flux-only, and a few more. The second step is the fine-tuning part. Again, fully dynamic, where you can pick and/or all of the "modules" like skin fix, face fix, K-Sampler Cycle fix, face swap, upscale, and more.

   Some parts have been added and adapted from other sources on the internet. An example is the flux image generation part. I did not make that one, but I did use other nodes to incorporate it into the workflow as another generation option within the list of "step 1" generation choices.

   There are options within options here that are constantly being rewritten, streamlined, and even a few unfinished (but hopefully working) parts. I'll try to keep this as short as possible while hopefully explaining a good amount.

   I have created this using a Windows box with an AMD 16GB VRAM card. It has taken me months to find the perfect balance of torch/Rocm/nodes/onnx/drivers and more. It might be a great idea to update in most cases, but this has taken me months, and I have no wish to update all and risk having to delete everything and re-install (I’m especially looking at you, ReActor. A great little node, but picky as hell)… Due to possible health and family concerns, I am trying to add this to a public repo asap and have not written everything down yet. This will take a number of custom nodes that I think some people will have problems with, and it might not be the most efficient, but it is working for me, and I have only been using ComfyUI image generation for about 10 months now, and I have never really gone over the basic steps. I just learned today that the ComfyUI Manager has a snapshot manager…damn. That could have saved me about a month of work alone.

❗️Each section in steps 1 and 2 will have a ‘Preview Image’ box. The workflow does not use any auto-save method. Please only right-click and choose Save As in the ‘Preview Image’ box (this is fine with batch images as well). Saving from the ‘Image Comparer’ or anything else might not work or give unexpected results. The only exception is the video module at the very end, that does save a file after each run.



Step 1:<br>
First, start by selecting one of several different ways to start within the "Step 1" section 'Choose' box.<br>
<br>
👉Generate Image from Text.<br> This is the most used, texted, and robust option. By default, it will create a batch of 4 images.
<ul>
  <li>You have the "set" box where you can choose:</li>
    <ul>
      <li>the checkpoint, steps, cfg, and other normal settings, including the width and height.
      <li>batch size should stay at 4, but I think 2 is doable, but not very tested.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>stop_at_clip_layer option to control clip encoding for lesser or greater detail/control.
      <li>✏️Vram debugging and clearing to increase speed and efficiency.</li>
    </ul>
   <li>The power lora loader by rgthree to load any lora's you wish.
   <li>The rgthree seed selector node makes seed control much easier and faster.
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>2nd positive prompt (Green as well) using Prompt database from benstaniford/comfy-prompt-db, to enable a quick selection of normally used prompts. This can be used in addition to the first positive prompt, the only positive prompt, or just left blank. It's all dynamic.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   <li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to send to "step 2"-image adjustment.
  </li>
</ul><br><br>
  
👉Generate Image from Image and Text.<br> By default, it will create a batch of 4 images. 
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
</ul><br><br>

👉Inpaint.<br> Can be tricky. The end of the section has a second model selected to go off a non-Inpaint model.<br>
❗️This input step is currently not working well. I am leaving it in hopes that it can be fixed at a later date.<br>
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
       <li>Note: Most modules in Step 2 have been updated to where you must select a safetensors file when needed, so this might not be used in most cases. This is a great way of mixing the different model parts together, like the face fix. I normally use Pony and Jaggernaut, and now have the option to generate an image with Pony, but I experiment with some fixes with other models to only fix the Fine tune Image, skin, face, or hands. </li></ul>
  <li>The preview image box should show the image generated, and is always the best way to save any image you choose.
  </li>
</ul><br><br>


👉Flux. <br>Use text to image generation with Fulx.
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
</ul><br><br>


👉Image to text<br> Uses 'comfyui-easy-use/easy imageInterrogator' node to read images into text descriptions. See how an AI describes images. You can also take the description and copy it to the 'Generate Image from Text' to change it anyway you want.
<ul>
   <li>Load Image box for any image you want the AI to 'see'.
  <li>The Set box will have many options you can change, like the model, steps, cfg, and so on.
    <ul>
      <li>batch size should stay at 4, but I think 2 is doable, but not very tested.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>'Generate Image' will take the text output and re-generate using only the text created, in batches, to compare it's discription from the main image to a copy to visually see the differences.
      <li>✏️Vram debugging and clearing to increase speed and efficiency. </li>
    </ul>
   <li>The rgthree seed selector node makes seed control much easier and faster.
   <li>The Positive and negative prompts are actually just text as output from the imageInterrogator node, and can't be directly edited.
   <li>The preview image box should show the image generated, and is always the best way to save any image you choose.
   <li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to send to "step 2"-image adjustment.
   </li>
</ul><br><br>

👉Florence2 image to text<br> Another type of image to text nodes that usually gives better or more detailed results. <br>
❗️Due to it needing a different model in order to first read the image, there are two sections in the 'Florence2 image to text' box.<br>
<ul>
   <li>Load Image box for any image you want the AI to 'see'. 
  <li>The Set box will have many options you can change, like the model, steps, cfg, and so on. Any options above the 'Generate Image?' option in the box is for the Florence2 model. Any option under 'Generate Image?' is for generating a new image using the output.
    <ul>
      <li>'Generate Image' will take the text output and re-generate using only the text created, in batches, to compare it's discription from the main image to a copy to visually see the differences.
       <li>batch size should stay at 4, but I think 2 is doable, but not very tested.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>✏️Vram debugging and clearing to increase speed and efficiency. </li>
    </ul>
   <li>The rgthree seed selector node makes seed control much easier and faster.
   <li>The Positive and negative prompts are actually just text output from the imageInterrogator node and can't be directly edited.
   <li>The preview image box should show the image generated, and is always the best way to save any image you choose.
   <li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to send to "step 2"-image adjustment.   
   </li>
</ul><br><br>

👉Restore Image<br>
Simple image restoration. The checkpoint selection for a model does nothing to the 'Restore Image' section and is only used in some areas of Step 2.<br>
<ul>
   <li>Load Image box for any image you want to restore. 
   <li>The Set box will have many options you can change for image restoration.
   <li>The Positive and negative prompts are actually just text as output from the imageInterrogator node, and can't be directly edited.
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show the image generated, and it is always the best way to save any image you choose.
   </li>
</ul><br><br>
✏️Note: Press the number 1 to jump back to the 'Step 1 Choice box' area.
<br><br><br>





Step 2:<br>
You can choose to enable any option, or options, to continue. This was added to make it easier to generate several times until you get a result you want to work with. Just click any yes or no button(s) in the ‘Choose’ menu at step 2. All modules are fully modular and made to work in any combination or number, but they can not change the direction (i.e., no Upscale before Face Swap. Only Face Swap and then Upscale.) So you can use the Face Fix and the Upscale while leaving Fine Tune, Face Swap, and Blend and Adjust Face Expression disabled, and it should just skip them. But I suggest only activating extra groups one at a time (You don't have to process more until you are ready, otherwise it will be a lot of wasted generations and slow things down. A good example is if I wanted to do Face Fix and Upscale, I would first do Face Fix, then come back to this menu (press '2' to jump here) and then enable Upscale, leaving Face Fix still on.)<br>

👉Fine Tune Image<br>
Will take the one image you selected from the previous batch of pictures and give it a re-touch. A light re-draw to the full image to help with artifacts or changes. This will give you a new batch of 4 images (same "Batch image" and shows "Image #" as above).
<ul>
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>You have the "set" box where you can choose :
    <ul>
      <li>the checkpoint, steps, cfg, and other normal settings. (Remember to mess with denoise to give the  generating model more or less freedom in the new image!)
      <li>’Number of Images’ is the number of images to generate in a batch. 4 is the best as I have found.
      <li>Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
      <li>stop_at_clip_layer option to control clip encoding for lesser or greater detail/control.
      <li>✏️Vram debugging and clearing to increase speed and efficiency.</li>
    </ul>
   <li>The rgthree seed selector node makes seed control much easier and faster.
   <li>The power lora loader by rgthree to load any lora's you wish.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   <li>And the ‘Batch Image’ box, where you can select the image you want to use in Step 2. This is an updated number scheme where the first image is 1, then 2, and so on. This will send *only* the image from the batch that you like to another modual, like upscale.
   </li>
</ul><br><br>


👉Skin Fix<br>
It is usually best to do this step before a Face or Hand Fix; however, I normally do not use this very often, as the results are usually bad, and you might spend a long time messing with the settings.
<ul>
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>You have the "set" box where you can choose several options.
   <li>The power lora loader by rgthree to load any lora's you wish.
   <li>The SkinDetailer box.
   <li>The pink masking box with three different windows that show which mask in choosen and how it is selected.
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   </li>
</ul><br><br>

👉Face Fix<br>
Regenerate a new face. Many faces you generate will have bad faces, like crooked eyes, or something wrong, but the body is perfect. This will help if you used too many loras and messed up the face.
<ul>
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>You have the "set" box where you can choose several options.
   <li>The power lora loader by rgthree to load any lora's you wish.
   <li>The FaceDetailer box.
   <li>The pink masking box with three different windows that show which mask in choosen and how it is selected.
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   </li>
</ul><br><br>

👉Hand Fix<br>
This will try to find and fix broken or messed-up fingers and hands.
<ul>
   <li>Main positive prompt (Green) and Negative prompt (Red).
   <li>Three small boxes under the prompt windows with detailer options.
   <li>The FaceDetailer box (with hand_* in UltralyticsDetectorProvider).
   <li>The pink masking box with three different windows that show which mask in choosen and how it is selected.
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   </li>
</ul><br><br>

👉Ksampler Cycle Fix<br>
Much like 'Fine Tune Image', this will redraw the image using cycles of the sampler and combine them. This is more focused on blending and refining any 'Fix', but can be used alone, without any other 'Fix' enabled.
<ul>
   <li> test </li>
</ul><br><br>

👉Face Swap<br>
Use face swap to change the face on the image to another face. ReActor is a fast and good faceswap, just very hard to install, atleast is was very difficult for me!
<ul>
   <li>First is the ReActor Fast Face Swap box. 
    <ul>
      <li>✏️The only real setting you will want to change is the 'input_faces_index' to search for faces (starting from left to right, 0,1, etc.) So if you only want to change the second person's face in a photo, you would just put 1. It can take some playing with before it finds the right thing. Remember that anything that is close to a face counts! Posters, people way in the background, the monalisa, a pile of garbage that kinda looks like a face if you squint really hard.</li>
    </ul>
   <li>Swap Choice box. A choice of auto-selecting up to 3 extra faces. This was put in to make it easier if you don't want to mess with the index count.
   <li>ReActor Face Booster. You can try using this, or disable it. The booster is usually a little much and can make things look odd.
   <li>Load Image box for any image you want to work on. 
   <li>Image Comparer (rgthree) allows you to compare the generated image to the original image.
   <li>The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
   </li>
</ul><br><br>

👉Face Swap (SimSwap)<br>
A different version of Face Swap is used. SimSwap is a higher-quality and more adjustable tool, but it is also very hard to get right.
<ul>
   <li> test </li>
</ul><br><br>

👉Blend and Adjust Face Expression<br>
Change the lighting, contrast, and other image settings with the ability to change some facial parameters.
<ul>
   <li> test </li>
</ul><br><br>

👉Upscale<br>
1x and 2x Upscale with a second preview window showing the 1x upscale version without the enlargement at full 1 to 1 quality. Upscales will have some light image enhancement and fine detail added(like hair, face, etc.).
<ul>
   <li> test </li>
</ul><br><br>

👉Video<br>
A small workflow that I added and changed a few things to make it where I  could dynamically just add the image I made through the workflow (it just saves me the time of saving files and swapping workflows)
<ul>
   <li> test </li>
</ul><br><br>


Would I ever do Face Fix and Face Swap at once? Well, yes. I have had several face swaps that looked odd because the face finder didn't work well and gave her a crooked jaw or no real lower lip...so A fresh regen of the face might help.<br>
Remember: Face Fix (Or regen) will capture ANY face (Picture on a shirt, poster, background guy, anything. But the Face Swap only works on one face unless you mess with the input_faces_index, and there is no way to get the Expressions node to work with more than one face, so you might find it useful to do a face regen on a photo of two hikers when they find a bear. Use Face Fix to tweak the facial features just about right, then do a face swap, and the face swap should overlay the face on top, not overwrite it. But just in case...now you can. Yay!<br>
<br>
✏️Note: Press the number 2 to jump back to the 'step 2 Choice(s) box' to enable different things!)
<br>
******************************************
<ul>
<li>Python version: 3.11.9
<li>AMD arch: gfx1201
<li>ROCm version: (7, 2)
<li>ComfyUI version: 0.11.1
<li>ComfyUI frontend version: 1.37.11
<li>Torch version: 2.10.0+rocm7.12.0a20260201
   </li>
</ul><br>
18 custom nodes:
   <ul>
<li>ComfyUI Impact Pack 8.28.2
<li>ComfyUI-Custom-Scripts 1.2.5
<li>rgthree-comfy 1.0.251211205
<li>ComfyUI-AdvancedLivePortrait 1.0.0
<li>ComfyUI-KJNodes 1.2.9
<li>ComfyUI-Easy-Use 1.3.4
<li>ComfyUI-Florence2 1.0.8
<li>ComfyUI_UltimateSDUpscale 1.7.2
<li>ComfyUI-ReActor 0.7.0-a1
<li>ComfyUI_essentials 1.1.0
<li>ComfyUI-Inpaint-CropAndStitch 3.0.7
<li>ComfyUI Impact Subpack 1.3.5
<li>ComfyUI-post-processing-nodes 1.0.1
<li>WAS Node Suite (Revised) 3.0.1
<li>lora-info 1.0.2
<li>ComfyUI-Notifications nightly
<li>comfyui-simswap nightly
<li>Prompt Database for ComfyUI unknown
      </li>
   </ul>

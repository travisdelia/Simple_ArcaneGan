
import gc
import math
import torch
import numpy as np
from encoded_video import EncodedVideo, write_video
from torchvision.transforms.functional import to_tensor, center_crop
import os




model = torch.jit.load('./ArcaneGANv0.4.jit').cuda().eval().half()

means = [0.485, 0.456, 0.406]
stds = [0.229, 0.224, 0.225]
from torchvision import transforms
norm = transforms.Normalize(means,stds)

def uniform_temporal_subsample(x: torch.Tensor, num_samples: int, temporal_dim: int = -3) -> torch.Tensor:
    t = x.shape[temporal_dim]
    assert num_samples > 0 and t > 0
    indices = torch.linspace(0, t - 1, num_samples)
    indices = torch.clamp(indices, 0, t - 1).long()
    return torch.index_select(x, temporal_dim, indices)

def makeEven(_x):
  return _x if (_x % 2 == 0) else _x+1

def short_side_scale(x: torch.Tensor, size: int, interpolation: str = "bilinear") -> torch.Tensor:
    c, t, h, w = x.shape
    if w < h: new_h, new_w = int(math.floor((float(h) / w) * size)), size
    else: new_h, new_w = size, int(math.floor((float(w) / h) * size))
    return torch.nn.functional.interpolate(x, size=(makeEven(new_h), makeEven(new_w)), mode=interpolation, align_corners=False)

norms = torch.tensor([0.485, 0.456, 0.406])[None,:,None,None].cuda()
stds = torch.tensor([0.229, 0.224, 0.225])[None,:,None,None].cuda()

def inference_step(vid, start_sec, duration, out_fps, interpolate):
    clip = vid.get_clip(start_sec, start_sec + duration)
    video_arr = torch.from_numpy(clip['video']).permute(3, 0, 1, 2)
    audio_arr = np.expand_dims(clip['audio'], 0)
    audio_fps = None if not vid._has_audio else vid._container.streams.audio[0].sample_rate
    x = uniform_temporal_subsample(video_arr,  duration * out_fps)
    x = short_side_scale(x, 512)
    x /= 255.
    x = x.permute(1, 0, 2, 3)
    x = norm(x)
    with torch.no_grad():
        output = model(x.to('cuda').half())
        output = (output * stds + norms).clip(0, 1) * 255.
        output_video = output.permute(0, 2, 3, 1).float().detach().cpu().numpy()
        if interpolate == 'Yes': output_video[1:] = output_video[1:]*(0.5) + output_video[:-1]*(0.5)
    return output_video, audio_arr, out_fps, audio_fps

def predict_fn(filepath, start_sec, duration, out_fps, interpolate):
    vid = EncodedVideo.from_path(filepath)
    for i in range(duration):
        video, audio, fps, audio_fps = inference_step(
            vid = vid,
            start_sec = i + start_sec,
            duration = 1,
            out_fps = out_fps,
            interpolate = interpolate
        )
        gc.collect()
        if i == 0:
            video_all = video
            audio_all = audio
        else:
            video_all = np.concatenate((video_all, video))
            audio_all = np.hstack((audio_all, audio))
    write_video(
        'out.mp4',
        video_all,
        fps=fps,
        audio_array=audio_all,
        audio_fps=audio_fps,
        audio_codec='aac'
    )
    del video_all
    del audio_all
    return 'out.mp4'

def main_loop():
    filename = input("Please enter the path to your video file: ")
    start_sec = int(input("Starting second in the video (default=0): ") or 0)
    duration = int(input("Duration in seconds (default=10): ") or 10)
    out_fps = int(input("Output FPS (default=30): ") or 30)
    interpolate_algorithm = input("Interpolate? Enter 'Yes' or 'No' (default='Yes'): ") or 'Yes'
    predict_fn(filename, start_sec, duration, out_fps, interpolate_algorithm)
    print("Process completed. The output file is named 'out.mp4'.")

if __name__ == "__main__":
    main_loop()



from diffusers import DiffusionPipeline
from dynaconf import Dynaconf
import torch
import random
import numpy as np


def test_model():
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['configs/settings.yaml'],
        environments=True,
        load_dotenv=True,
    )
    MAX_SEED = np.iinfo(np.int32).max
    device = torch.device(settings.model.device if torch.cuda.is_available() else "cpu")
    dtype = torch.bfloat16
    pipe = DiffusionPipeline.from_pretrained(
        settings.model.id,
        torch_dtype=dtype,
        use_safetensors=True,
        cache_dir=settings.model.cache_dir,
        low_cpu_mem_usage=False
    ).to(device)
    seed = random.randint(0, MAX_SEED)
    generator = torch.Generator().manual_seed(seed)
    image = pipe(
        prompt='a tiny astronaut hatching from an egg on the moon',
        width=1024,
        height=1024,
        num_inference_steps=4,
        generator=generator,
        guidance_scale=0.0
    ).images[0]

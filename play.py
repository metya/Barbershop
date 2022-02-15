import streamlit as st
from PIL import Image
from pathlib import Path
from io import StringIO, BytesIO
import time
from natsort import natsorted

from main import main
from align_face import func_align


class align_args:
    unprocessed_dir='unprocessed'
    output_dir='input/face'

    output_size=1024
    seed=None
    cache_dir='cache'

    ###############
    inter_method='bicubic'

class args:
    # I/O arguments
    input_dir='input/face'
    output_dir='output'
    im_path1='16.png'
    im_path2='15.png'
    im_path3='117.png'
    sign='realistic'
    smooth=5

    # StyleGAN2 setting
    size=1024
    ckpt="pretrained_models/ffhq.pt"
    channel_multiplier=2
    latent=512
    n_mlp=8

    # Arguments
    device='cuda'
    seed=None
    tile_latent=False
    opt_name='adam'
    learning_rate=0.01
    lr_schedule='fixed'
    save_intermediate=False
    save_interval=300
    verbose=False
    seg_ckpt='pretrained_models/seg.pth'

    # Embedding loss options
    percept_lambda=1.0
    l2_lambda=1.0
    p_norm_lambda=0.001
    l_F_lambda=0.1
    W_steps=1100
    FS_steps=250

    # Alignment loss options
    ce_lambda=1.0
    style_lambda=4e4
    align_steps1=140
    align_steps2=100

    # Blend loss options
    face_lambda=1.0
    hair_lambda=1.0
    blend_steps=400


st.title('Barbershop GAN')
st.header('Привет! Тут ты можешь сделать себе новую прическу и посмотреть какой ты странный.')

st.write('Загрузи сюда свою фотку, которую ты хочешь заюзать.')
target_face = st.file_uploader('Твоя фотка', type=['png', 'jpg', 'jpeg'])
if target_face is not None:
    bytes_data = target_face.getvalue()
    bytes = BytesIO(bytes_data)
    target_face_image = Image.open(bytes)
    target_face_image.save(f'unprocessed/{target_face.name}')
    im1_name = target_face.name.split('.')[0] + '.png'
    args.im_path1 = im1_name
    st.image(target_face_image)
    
structure_pic = st.selectbox('Выбери Structure из списка сайдбара', range(31))
appearance_pic = st.selectbox('Выбери Appearence из списка сайдбара', range(31))

args.im_path2 = f'{structure_pic}.png'
args.im_path3 = f'{appearance_pic}.png'

if st.button('Сделать причу!'):
    st.write('Начинаю делать прическу! Это займет некоторое время. Придется подождать')
    with st.spinner('Ищу лицо на фотке и делаю выравнивание'):
        func_align(align_args)
    st.success('Лицо выравнено!')
    with st.spinner('Припиливаю прическу!'):
        main(args)
    st.success('Готово!')
    
    output = Image.open(f'output/{target_face.name.split(".")[0]}_{structure_pic}_{appearance_pic}_realistic.png')
    st.image(output)


faces = natsorted([str(im_path) for im_path in Path('input/face/').glob('*')])
with st.sidebar:
    for i, face in enumerate(faces[:30]):
        col1, col2 = st.columns(2)
        col1.image(Image.open(face), width=150)
        col2.text(Path(face).stem)
    if st.button('Next 60'):
        for i, face in enumerate(faces[30:90]):
            col1, col2 = st.columns(2)
            col1.image(Image.open(face), width=150)
            col2.text(Path(face).stem)

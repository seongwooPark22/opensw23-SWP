# OpensourceSW 입문 Project
> Original Code from ibaiGorordo's [ONNX-CREStereo-Depth-Estimation](https://github.com/ibaiGorordo/ONNX-CREStereo-Depth-Estimation)
### Team Introduction
##### 박성우 202211298 프로젝트 중 모든 역할

### Topic Introduction
## *Stereo Depth Estimation*
해당 Github Repo에서는
한번에 두개의(왼쪽과 오른쪽으로 편차가 있는 Stereo) 이미지 혹은 동영상정보들이
인풋으로 들어가게 되고 ONNX기반의 CREStereo 모델을 통하여 두 인풋을 통해 하나의
depth를 도출해주는 Python Scripts를 다룹니다.

> ONNX란? 간단하게 설명하면, pytorch같은 tensorflow 서로 다른 두 환경에서 만들어진 모델들을
> 서로 호환가능하게 ONNX로 변환하여 ONNX runtime위에서 실행할 수 있게 해주는겁니다.

Depth Map은 컴퓨터 그래픽스에서 요긴하게 이용되는 요소입니다.
그렇기에 게임에서 볼 수 있는 각종 그래픽 효과들을 만들 때도 많이 사용되고 있습니다.
현대의 대부분의 GPU는 하드웨어 레벨에서 이를 위한 depth testing 지원하고 있습니다.

* Depth Map을 활용한 Outline 효과 : https://www.ronja-tutorials.com/post/019-postprocessing-outlines/
* Pure Depth SSAO : https://theorangeduck.com/page/pure-depth-ssao

하지만 사진등은(비트맵) 픽셀에 대한 정보만을 가지고 있지 깊이 정보를 가지고 있지 않기 때문에
일반 사진, 영상에서 이 depth을 그냥 만들어낼 수는 없습니다.
그런 일반 사진에서 depth맵을 estimation하는 것이 이 Repo에서 다루고 있는 것입니다.

### Results(Image)
### Input1
https://vision.middlebury.edu/stereo/data/scenes2003/
위 링크의 cones/im2, cones/im6
URL로 바로 실행하는 구조이다.
### Result1
![!result1](./readme_img/temp_result1.png)
---
### Input2
https://vision.middlebury.edu/stereo/data/scenes2003/
위 링크의 teddy/im2, teddy/im6
URL로 바로 실행하는 구조이다.
### Result2
![!result3](./readme_img/temp_result2.png)
Stereo depth estimation on the cones images from the Middlebury dataset (https://vision.middlebury.edu/stereo/data/scenes2003/)
---
## Results(Video)
### Input
사용한 유튜브 영상 URL : https://youtu.be/Yui48w71SG0
### Results
![!result3](./readme_img/vid_result1.png)
---
## Analysis/Visualization
## Installation / Inference
#### My Environment
* Macbook M1 Chip
* python3.11
* No Nvidia GPU

1. git clone
```
git clone https://github.com/seongwooPark22/opensw23-SWP.git
cd opensw23-SWP
```
2. Install requirements 

reqirements.txt 내부를 이렇게 바꿔주세요

* 만약 NVIDIA GPU를 사용하는 컴퓨터라면 -> `onnxruntime-gpu` -> 변경X
* 만약 NVIDIA GPU를 사용하지 않는 컴퓨터라면 : `onnxruntime-gpu` -> `onnxruntime`

수정한 후 -> `pip install -r requirements.txt` 실행

Video Inference는 Youtube 영상의 URL을 사용하기때문에
이를 실행하기 위해서는 yt-dlp를 설치해야합니다.
`pip install yt-dlp`

3. Download Pre-Trained Model
### ONNX Model

The models were converted from the Pytorch implementation below by [PINTO0309](https://github.com/PINTO0309)
https://github.com/PINTO0309/PINTO_model_zoo/tree/main/284_CREStereo
The License of the models is Apache-2.0 License: https://github.com/megvii-research/CREStereo/blob/master/LICENSE

위 링크에서 .sh파일 받아 실행하여 생성된 파일을 models폴더로 옮겨 주세요
```
sh [file_you_download]
```
주의
> 윈도우 사용자라면, .sh 파일을 실행하기 위해 git bash를 사용하거나
> Cygwin 등을 사용하는 방법이 있으니 참고해주세요

저는 `download_iter05_tensorrt.sh`로 모델을 다운로드 받았습니다.

1. Inference
* Image inference (URL)
```
python image_depth_estimation.py
```
* Video Inference (Youtube)
```
python video_depth_estimation.py
```
위의 코드로 실행하여 결과를 볼 수 있습니다.
대상 URL을 변경하고 싶다면 스크립트 내부에 있는 경로를 직접 수정해야합니다.
이는 개선사항이기 때문에 후에 수정을 시도할 것입니다.
### Presentation

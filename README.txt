mkdir -p /dacx/videoprocess/face_comparison

cd /dacx/videoprocess/face_comparison
git clone <face_comparison REPO>

mkdir /dacx/videoprocess/face_comparison/face_comparison_uploads 
mkdir /dacx/videoprocess/face_comparison/logs 


#logs
/dacx/videoprocess/face_comparison/logs/face_comparison.log

cd /dacx/videoprocess/face_comparison/face_comparison
docker-compose down
docker-compose up --build

API will be running on 8501 port


JSON Response SUCCESS: {"ID":"UNIQUE ID-STRING","distance":0.615,"code":1}
JSON Response FAILURE: {"ID":"UNIQUE ID-STRING","distance":-1,"code":0}


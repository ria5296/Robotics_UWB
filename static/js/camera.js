document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const switchButton = document.getElementById('switchButton');
    const errorMsg = document.getElementById('errorMsg');

    let currentStream = null;
    let facingMode = 'environment'; // 'environment'는 후면, 'user'는 전면

    // 카메라 시작 함수
    async function startCamera() {
        try {
            if (currentStream) {
                stopCamera();
            }

            const constraints = {
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: facingMode
                },
                audio: false
            };

            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            video.srcObject = stream;
            currentStream = stream;
            errorMsg.textContent = '';
        } catch (err) {
            console.error('카메라 에러:', err);
            errorMsg.textContent = '카메라를 시작할 수 없습니다. ' + err.message;
        }
    }

    // 카메라 정지 함수
    function stopCamera() {
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
            video.srcObject = null;
            currentStream = null;
        }
    }

    // 카메라 전환 함수
    function switchCamera() {
        facingMode = facingMode === 'environment' ? 'user' : 'environment';
        startCamera();
    }

    // 이벤트 리스너 등록
    startButton.addEventListener('click', startCamera);
    stopButton.addEventListener('click', stopCamera);
    switchButton.addEventListener('click', switchCamera);

    // 페이지 로드 시 자동으로 카메라 시작
    startCamera();

    // 페이지 종료 시 카메라 정지
    window.addEventListener('beforeunload', stopCamera);
});
const cutImg = (e) => {
    var btn = document.getElementById("btn");
    btn.value = "画像を処理しています..."
    var zeus = document.getElementById("zeus-says");
    zeus.innerHTML = "ぬぬぬ...画像を処理しとるぞ..."
    const reader = new FileReader();
    const imgReader = new Image();
    const maxLength = 640;
    reader.onloadend = () => {
        imgReader.onload = () => {
            const imgType = imgReader.src.substring(5, imgReader.src.indexOf(';'));
            if (imgReader.width < imgReader.height){
                var imgHeight = maxLength;
            var imgWidth = imgReader.width * (imgHeight / imgReader.height);
            } else {
            var imgWidth = maxLength;
            var imgHeight = imgReader.height * (imgWidth / imgReader.width);
            }
            const canvas = document.createElement('canvas');
            canvas.width = imgWidth;
            canvas.height = imgHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(imgReader,0,0,imgWidth,imgHeight);
            var img = document.getElementById("render_image");
            img.style.visibility = 'hidden';
            var zeus = document.getElementById("zeus-says");
            zeus.innerHTML = "顔の部分を探しているからもう少し待ってくれよの..."
            var btn = document.getElementById("btn");
            btn.value = "顔の部分を探しています..."
            console.log(canvas.toDataURL(imgType).replace(/data:.*\/.*;base64,/, ''))
            
            // 既定のオプションには * が付いています
            fetch("CUT_URL", {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, *cors, same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'include', // include, *same-origin, omit
            headers: {
            'Content-Type': 'application/json'// 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: 'follow', // manual, *follow, error
            referrerPolicy: 'strict-origin', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
            body: JSON.stringify({input_text: canvas.toDataURL(imgType).replace(/data:.*\/.*;base64,/, '')}) // 本文のデータ型は "Content-Type" ヘッダーと一致させる必要があります
            }).then(response => {
            return response.json()
            })
            .then(data => {
            if (data.result.is_face == "True"){
                var img = document.getElementById("render_image");
                img.src = "data:image/jpeg;base64," + data.result.img;
                img.style.visibility = 'visible';
                btn.style.visibility = 'visible';
                var zeus = document.getElementById("zeus-says");
                zeus.innerHTML = "顔の部分はここであっとるかの？よければ<strong>OKボタン</strong>をクリックしてくれ！！"
                btn.value = "OK！！";
            }else{
                btn.value = "顔の部分が検出できませんでした、他の画像を選択してください"
            }
            })
        }
      imgReader.src = reader.result;
    }
    reader.readAsDataURL(e.files[0]);
  }

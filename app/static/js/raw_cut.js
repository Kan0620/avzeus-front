const cutImg = (e) => {
    var btn = document.getElementById("btn");
    btn.value = "画像を処理しています..."
    var zeus = document.getElementById("zeus-says");
    const lang = document.getElementById("select").value;
    if (lang == "zh") {
        zeus.innerHTML = "嗯... 我们正在处理图像..."
    } else if (lang == "en"){
        zeus.innerHTML = "Mmmm... I'm processing the image..."
    } else{
        zeus.innerHTML = "ぬぬぬ...画像を処理しとるぞ..."
    }
    
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
            const lang = document.getElementById("select").value;
            if (lang == "zh") {
                zeus.innerHTML = "我们正在寻找脸部的部分，所以你必须再等一等......"
            } else if (lang == "en"){
                zeus.innerHTML = "I'm looking for the face part, just need to wait a little longer..."
            } else{
                zeus.innerHTML = "顔の部分を探しているからもう少し待ってくれよの..."
            }
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
                const lang = document.getElementById("select").value;
                if (lang == "zh") {
                    zeus.innerHTML = "这个地方适合做脸吗？ 如果你喜欢，请点击 <strong>OK</strong>按钮!"
                } else if (lang == "en"){
                    zeus.innerHTML = "Is this the right place for the face? Click the <strong>OK button</strong> if you like!"
                } else{
                    zeus.innerHTML = "顔の部分はここであっとるかの？よければ<strong>OKボタン</strong>をクリックしてくれ！！"
                }
                btn.value = "OK";
            }else{
                var zeus = document.getElementById("zeus-says");
                const lang = document.getElementById("select").value;
                if (lang == "zh") {
                    zeus.innerHTML = "无法找到面部部分，请选择其他图片。"
                } else if (lang == "en"){
                    zeus.innerHTML = "The face part could not be found, please select another image."
                } else{
                    zeus.innerHTML = "顔の部分が見つからなかったぞい、他の画像を選んどくれんかの..."
                }
                btn.value = "顔の部分が検出できませんでした、他の画像を選択してください"
            }
            })
        }
      imgReader.src = reader.result;
    }
    reader.readAsDataURL(e.files[0]);
  }

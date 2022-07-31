function toResult() {
    
    var sub_btn = document.getElementById("btn");
    if (sub_btn.value == "お願いします！！"){
      sub_btn.value = "少々お待ちください"
      var img = document.getElementById("render_image");
      fetch("PREDICT_URL", {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'include', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'

        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'strict-origin', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify({input_text: img.src.replace(/data:.*\/.*;base64,/, '')}) // 本文のデータ型は "Content-Type" ヘッダーと一致させる必要があります
      }).then(response => {
        return response.json()
      })
      .then(data => {
        // window.open("https://avzeus-front.herokuapp.com/img-rec-result/"+data.result.rec_actress_id,
        // '_blank'
        // );
        window.location.href = "https://www.av-zeus.com/img-rec-result/"+data.result.rec_actress_id
      })

    }else if (sub_btn.value == "顔の部分を探しています..."){
      window.alert("画像の顔部分を探しています。少々お待ちください。")
    }
    else if(sub_btn.value == "顔の部分が検出できませんでした、他の画像を選択してください"){
      window.alert("他の画像を選択してください")
    }
    else{
      window.alert("画像を選択してください")
    }
    }
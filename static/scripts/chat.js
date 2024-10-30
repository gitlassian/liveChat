document.addEventListener("DOMContentLoaded", () => {
    const log = document.getElementById("log");
    const button = document.querySelector('[name=button]')
    const input = document.querySelector('[name=message_input]')

    let nick

    document.cookie.split(";").forEach((part) => {
        if (part.split("=")[0]==="nick")
            nick = part.split("=")[1]
    });

    const websocket = new WebSocket('http://localhost:80/');

    websocket.onopen = () => {
        websocket.send([nick])
    }

    button.onclick = () => {
        if((input.value).length>1){
            websocket.send(input.value)
            input.value = ""
        }
    }
    

    websocket.onmessage = (message) => {
        data = JSON.parse(message.data)

        nick = document.createElement("span")
        text = document.createElement("span")
        
        nick.innerHTML = data[2]
        nick.style.color = data[1]
        text.innerHTML = ": "+data[0]
        log.appendChild(nick)
        log.appendChild(text)
        log.innerHTML = log.innerHTML + "<br>";
    }
    websocket.onclose = (event) => {
        console.log("WebSocket connection closed: ", event);
    };
}, false)
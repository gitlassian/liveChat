document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("[name=nick]")
    const start = document.getElementById("start")

    let request = (nick) => { return new Request("/login", {
            method: "POST",
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify({"nick": nick})
        }
    )}

    start.onclick = async () => {
        console.log(input.value)
        if (input.value != ""){
            let response = await fetch(request(input.value))
            let data = await response.json() 
            if (data["redirect"] == true){
                let date = new Date(Date.now() + 1800e3);
                date = date.toUTCString();
                document.cookie = "nick=" + input.value + "; expires=" + date;
                document.location = "chat"
            }
            else{
                alert("Try another name")
            }
        }
    }
}, false)
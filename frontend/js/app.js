
async function send() {
  let input = document.getElementById("msg");
  let text = input.value;

  document.getElementById("box").innerHTML += "<div>Sen: " + text + "</div>";

  let res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: text})
  });

  let data = await res.json();

  document.getElementById("box").innerHTML += "<div>Bot: " + data.reply + "</div>";

  input.value = "";
}

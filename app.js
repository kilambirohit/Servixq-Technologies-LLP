function start() {
    const url = document.getElementById("url").value;

    document.getElementById("status").innerText =
        "⚠️ Go to GitHub → Actions → Run workflow manually";

    console.log("URL:", url);
}

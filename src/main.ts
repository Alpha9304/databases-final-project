import "./style.css";

const memeAPI = "https://api.imgflip.com/get_memes";

console.log(memeAPI);

//get needed document elements
const memeSection: HTMLElement = document.getElementById("meme") as HTMLElement;
const topTextInput: HTMLInputElement = document.getElementById("input-top-text") as HTMLInputElement;
const bottomTextInput: HTMLInputElement = document.getElementById("input-bottom-text") as HTMLInputElement;
const errorText: HTMLElement = document.getElementById("error") as HTMLElement;
const goButton: HTMLButtonElement = document.getElementById("submit") as HTMLButtonElement;

function createMemeText(which: string): HTMLElement{
    const text: HTMLElement = document.createElement("h2");
    if(which === "top") {
        if(topTextInput.value === ""){
            throw new Error("Please enter text into both fields.");
        } else {
            text.innerText = topTextInput.value;
        }
    } else {
        if(bottomTextInput.value === ""){
            throw new Error("Please enter text into both fields.");
        } else {
            text.innerText = bottomTextInput.value;
        }
    }

    return text;
}

function generateMeme() {
    memeSection.innerHTML = "";
    errorText.innerText = "";
    topTextInput.classList.add("border-stone-200");
    topTextInput.classList.remove("border-red-200");

    bottomTextInput.classList.add("border-stone-200");
    bottomTextInput.classList.remove("border-red-200");
    try {
        const topText: HTMLElement = createMemeText("top") as HTMLElement;
        const bottomText: HTMLElement = createMemeText("bottom") as HTMLElement;
        memeSection.appendChild(topText);
        memeSection.appendChild(bottomText);
    } catch (error) {
        errorText.innerText = (error as Error).message;
        
        if(topTextInput.value === ""){
            topTextInput.classList.remove("border-stone-200");
            topTextInput.classList.add("border-red-200");
        }

        if(bottomTextInput.value === ""){
            bottomTextInput.classList.remove("border-stone-200");
            bottomTextInput.classList.add("border-red-200");
        }
    }
}

goButton.addEventListener("click", generateMeme);



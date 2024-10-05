import "./style.css";

const memeAPI = "https://api.imgflip.com/get_memes";

console.log(memeAPI);

//get needed document elements
const memeSection: HTMLElement = document.getElementById("meme") as HTMLElement;
const topTextInput: HTMLInputElement = document.getElementById("input-top-text") as HTMLInputElement;
const bottomTextInput: HTMLInputElement = document.getElementById("input-bottom-text") as HTMLInputElement;
const errorText: HTMLElement = document.getElementById("error") as HTMLElement;
const goButton: HTMLButtonElement = document.getElementById("submit") as HTMLButtonElement;

//define custom types
type Meme = {
    id: string;
    name: string;
    url: string;
    width: Number;
    height: Number;
    box_count: Number;
}

type Data = {
    memes: Meme[];
}
type memeAPIResponse = {
    success: boolean;
    data: Data;
}

function clearInputBoxes(){
    topTextInput.value = "";
    bottomTextInput.value = "";
}

function createMemeText(which: string): HTMLElement{
    const text: HTMLElement = document.createElement("h2");
    text.classList.add("absolute");
    text.classList.add("text-xl");
    text.classList.add("left-1/2");
    if(which === "top") {
        if(topTextInput.value === ""){
            throw new Error("Please enter text into both fields.");
        } else {
            text.classList.add("top-0");
            text.innerText = topTextInput.value;
        }
    } else {
        if(bottomTextInput.value === ""){
            throw new Error("Please enter text into both fields.");
        } else {
            text.classList.add("bottom-0");
            text.innerText = bottomTextInput.value;
        }
    }

    return text;
}

async function generateMeme() {
    memeSection.innerHTML = "";
    errorText.innerText = "";
    topTextInput.classList.add("border-stone-200");
    topTextInput.classList.remove("border-red-200");

    bottomTextInput.classList.add("border-stone-200");
    bottomTextInput.classList.remove("border-red-200");
    

    

    try {
        
        const memeContainer : HTMLElement = document.createElement("div");
        memeContainer.classList.add("relative", "w-full", "h-[600px]", "bg-contain", "bg-cover");
        

        const response : Response = await fetch('https://api.imgflip.com/get_memes');
        const result: memeAPIResponse = await response.json();
        
        const choice = Math.floor((Math.random() * result.data.memes.length));
        const chosenImgURL = result.data.memes[choice].url;

        memeContainer.style.backgroundImage = `url(${chosenImgURL})`;
        memeContainer.classList.add("bg-black");

        //const textContainer : HTMLElement = document.createElement("div");
        const topText: HTMLElement = createMemeText("top") as HTMLElement;
        const bottomText: HTMLElement = createMemeText("bottom") as HTMLElement;
        memeContainer.appendChild(topText);
        memeContainer.appendChild(bottomText);
        memeContainer.classList.add("bg-transparent");

        //memeContainer.appendChild(memeContainer);
        memeSection.appendChild(memeContainer);
        
        /*
        const topText: HTMLElement = createMemeText("top") as HTMLElement;
        const bottomText: HTMLElement = createMemeText("bottom") as HTMLElement;
        memeSection.appendChild(topText);
        memeSection.appendChild(bottomText);
        
        const response : Response = await fetch('https://api.imgflip.com/get_memes');
        const result: memeAPIResponse = await response.json();
        
        const choice = Math.floor((Math.random() * result.data.memes.length));
        const chosenImgURL = result.data.memes[choice].url;

        const imageSection : HTMLImageElement = document.createElement("img");
        imageSection.src = chosenImgURL;

        memeSection.appendChild(imageSection);*/
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

//clear input boxes on reload
clearInputBoxes();
    
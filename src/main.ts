import "./style.css";

//define custom types
type Meme = {
  id: string;
  name: string;
  url: string;
  width: Number;
  height: Number;
  box_count: Number;
};

type Data = {
  memes: Meme[];
};

type memeAPIResponse = {
  success: boolean;
  data: Data;
};

type cachedResponse = {
  response: memeAPIResponse | null;
  date: Date | null;
};

const memeAPI: string = "https://api.imgflip.com/get_memes";

//get needed document elements
const memeSection: HTMLElement = document.getElementById("meme") as HTMLElement;
const topTextInput: HTMLInputElement = document.getElementById(
  "input-top-text",
) as HTMLInputElement;
const bottomTextInput: HTMLInputElement = document.getElementById(
  "input-bottom-text",
) as HTMLInputElement;
const errorText: HTMLElement = document.getElementById("error") as HTMLElement;
const goButton: HTMLButtonElement = document.getElementById(
  "submit",
) as HTMLButtonElement;

//create API response cache
const cache: cachedResponse = { response: null, date: null };

//function to clear input boxes
function clearInputBoxes(): void {
  topTextInput.value = "";
  bottomTextInput.value = "";
}

//helper function to create meme text
function createMemeText(which: string): HTMLElement {
  const text: HTMLElement = document.createElement("h2");
  text.classList.add("absolute");
  text.classList.add("left-1/2");
  text.classList.add("transform", "-translate-x-1/2");
  text.classList.add(
    "text-6xl",
    "text-white",
    "font-extrabold",
    "text-outline",
  );
  if (which === "top") {
    if (topTextInput.value === "") {
      throw new Error("Please enter text into both fields.");
    } else {
      text.classList.add("top-0");
      text.innerText = topTextInput.value.toUpperCase();
    }
  } else {
    if (bottomTextInput.value === "") {
      throw new Error("Please enter text into both fields.");
    } else {
      text.classList.add("bottom-0");
      text.innerText = bottomTextInput.value.toUpperCase();
    }
  }

  return text;
}

//helper function to fetch data from the API
async function getResponse(): Promise<memeAPIResponse> {
  const response: Response = await fetch(memeAPI);
  const data: memeAPIResponse = await response.json();
  return data;
}

//helper function to get the meme and use the cache if a day has not passed
async function getMeme(): Promise<memeAPIResponse> {
  const today: Date = new Date();
  if (cache.response === null || cache.date === null) {
    const data: memeAPIResponse = await getResponse();
    cache.response = data;
    cache.date = today;
    return data;
  } else {
    if (today.getTime() < cache.date.getTime() + 60 * 60 * 24 * 1000) {
      return cache.response;
    } else {
      const data: memeAPIResponse = await getResponse();
      cache.response = data;
      cache.date = today;
      return data;
    }
  }
}

//function to generate a new meme
async function generateMeme(): Promise<void> {
  memeSection.innerHTML = "";
  errorText.innerText = "";
  topTextInput.classList.add("border-stone-200");
  topTextInput.classList.remove("border-red-200");

  bottomTextInput.classList.add("border-stone-200");
  bottomTextInput.classList.remove("border-red-200");

  try {
    const memeContainer: HTMLElement = document.createElement("div");
    memeContainer.classList.add(
      "relative",
      "w-full",
      "h-[600px]",
      "bg-contain",
      "bg-[length:auto_100%]",
      "bg-no-repeat",
      "bg-center",
    );

    const result: memeAPIResponse = await getMeme();

    const choice: number = Math.floor(Math.random() * result.data.memes.length);
    const chosenImgURL: string = result.data.memes[choice].url;

    memeContainer.style.backgroundImage = `url(${chosenImgURL})`;
    const topText: HTMLElement = createMemeText("top") as HTMLElement;
    const bottomText: HTMLElement = createMemeText("bottom") as HTMLElement;
    memeContainer.appendChild(topText);
    memeContainer.appendChild(bottomText);
    memeContainer.classList.add("bg-transparent");
    memeSection.classList.add("bg-black");
    memeSection.appendChild(memeContainer);
  } catch (error) {
    errorText.innerText = (error as Error).message;

    if (topTextInput.value === "") {
      topTextInput.classList.remove("border-stone-200");
      topTextInput.classList.add("border-red-200");
    }

    if (bottomTextInput.value === "") {
      bottomTextInput.classList.remove("border-stone-200");
      bottomTextInput.classList.add("border-red-200");
    }
  }
}

//function to generate a meme on enter
function generateOnEnter(event: KeyboardEvent): void {
  if (event.key === "Enter") {
    generateMeme();
  }
}

//add needed event listeners
goButton.addEventListener("click", generateMeme);
topTextInput.addEventListener("keydown", generateOnEnter);
bottomTextInput.addEventListener("keydown", generateOnEnter);

//clear input boxes on reload
clearInputBoxes();

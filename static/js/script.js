let songName = document.getElementById("songName");
let currentTimeofSong = document.getElementById("currentTimeofSong");
let totalTimeofSong = document.getElementById("totalTimeofSong");
let bgImg = document.getElementById("bgImg");
let content = document.getElementById("content");
let playPauseButton = document.getElementById("playPauseButton");
let progressBar = document.getElementById("progressBar");
let card = document.getElementById("card");
let lyrics = document.getElementById('lyrics');
let likeBtn = document.getElementById("likeBtn");
let repeatBtn = document.getElementById("repeatBtn");
let shuffleBtn = document.getElementById("shuffleBtn");
let shareBtn = document.getElementById("shareBtn");
let moreBtn = document.getElementById("moreBtn");
let homeBtn = document.getElementById("homeBtn");
let searchBtn = document.getElementById("searchBtn");
let favSongsBtn = document.getElementById("favSongsBtn");
let accountBtn = document.getElementById("accountBtn");
let lyricsContent = document.getElementsByClassName("lyricsContent");
let backContainer = document.getElementById("backContainer")
songList = document.getElementsByClassName("songList");
let mainTitle = document.getElementById("mainTitle");
let title = document.getElementById("title");
let video = document.getElementById("myVideo");
// let searchDefaultData = document.getElementById("searchDefaultData")
// let dataAllSongs = document.getElementsByClassName("dataAllSongs")
let song;
let songLyrics;
let songBg;
let lyricsData;
let audio;
let strName;
let count = 0;

// ******data from server*********
let datasongNames = document.getElementsByClassName("datasongNames")
let songNameArr = [];
let songIndex = [];

Array.from(datasongNames).forEach((element, index) => {
    songIndex.push(index)
    songNameArr.push(element.innerHTML);
})

let datasongLyrics = document.getElementsByClassName("datasongLyrics")
let songLyricsArr = []
Array.from(datasongLyrics).forEach((elem) => {
    songLyricsArr.push(elem.innerHTML)
})
let songAlbumArr = []
let datasongAlbum = document.getElementsByClassName("datasongAlbum")
Array.from(datasongAlbum).forEach((elem) => {
    songAlbumArr.push(elem.innerHTML)
})
let songBgArr = []
let datasongBg = document.getElementsByClassName("datasongBg")
Array.from(datasongBg).forEach((elem) => {
    songBgArr.push(elem.innerHTML)
})
let songArtistArr = []
let datasongArtist = document.getElementsByClassName("datasongArtist")
Array.from(datasongArtist).forEach((elem) => {
    songArtistArr.push(elem.innerHTML)
})
let serverData = {
    songs: songNameArr,
    lyrics: songLyricsArr,
    bg: songBgArr,
    album: songAlbumArr,
    artist: songArtistArr

}
console.log(serverData)

// ******data from server*********
let noOfSongs = songNameArr.length;
let index = Math.floor(Math.random() * noOfSongs);

// index = noOfSongs - 1;
// index = 2;
//console.log(index);
songSelection(index);

function songSelection(index) {
    song = `/static/assets/songs/${serverData.songs[index]}`;
    songLyrics = `/static/assets/lyrics/${serverData.lyrics[index]}`;
    songBg = `/static/assets/bg/${serverData.bg[index]}`;
    try {

        if (audio.currentTime > 0) {
            audio.currentTime = audio.duration;
        }
        video.load();
    } catch (error) {
        video.load();
    }



    audio = new Audio(song);
    strName = (`${serverData.songs[index]}`).replace(/_/g, " ").replace(/.mp3/i, "")
    try {
        Array.from(songList).forEach((elem, i) => {
            if (i == index) {
                elem.classList.add("active");
                elem.setAttribute("aria-current", "true")
            } else {
                elem.classList.remove("active");
                elem.setAttribute("aria-current", "false")
            }
        })
    } catch (error) {
        // console.log(error)
    }
    mainTitle.innerHTML = strName;
    document.title = strName;
    songName.innerHTML = strName;
    // console.log(serverData.bg[index])

    video.innerHTML = `<source src="${songBg}" type="video/mp4">`;

    if (strName.length > 25) {
        mainTitle.setAttribute("style", "font-size:large");
        songName.setAttribute("style", "font-size:x-small;padding-left: 10px;");
    } else {
        mainTitle.setAttribute("style", "font-size:large");
        songName.setAttribute("style", "font-size:small;padding-left: 10px;");
    }
    //console.log(`${serverData.songs[index]}`)
    fetch(songLyrics).then(function(Response) {
        return Response.text();
    }).then(function(data) {
        lyricsData = parseLyrics(data);
    })
    if (count > 0) {
        audio.autoplay = true;
        video.autoplay = true;
        playPauseButton.innerHTML = `<i style="transform: scale(1.6)" class="fa-solid fa-pause"></i>`;
    } else {
        video.autoplay = false;
    }
    let catches;
    audio.addEventListener('timeupdate', () => {
        val = audio.currentTime / audio.duration * 100;
        // console.log(val)
        progressBar.value = val;
        currentTimeofSong.innerHTML = new Date(audio.currentTime * 1000).toISOString().substr(14, 5);
        totalTimeofSong.innerHTML = new Date(audio.duration * 1000).toISOString().substr(14, 5);
        clearInterval(catches)
        try {
            lyricsWriter(lyricsData, audio.currentTime);
        } catch (error) {
            catches = setInterval(lyricsWriter(lyricsData, audio.currentTime), 1000);
        }
    })
    count++;
}
let catching;

function lyricsWriter(lyricsData, time) {
    let itl;
    clearInterval(itl)
    try {
        const index = syncLyrics(lyricsData, time)
    } catch (error) {
        itl = setInterval((lyricsData, audio.currentTime), 1000)
    }
    const index = syncLyrics(lyricsData, time);
    if (index == null) return;
    let diffs = lyricsData.length - index - 1;
    if (diffs >= 0) {
        lyricsContent[0].innerHTML = lyricsData[index].text.fontsize(5);
    } else {
        lyricsContent[0].innerHTML = "";
    }
    if (diffs >= 1) {
        lyricsContent[1].innerHTML = lyricsData[index + 1].text;
    } else {
        lyricsContent[1].innerHTML = "";
    }
    if (diffs >= 2) {
        lyricsContent[2].innerHTML = lyricsData[index + 2].text;
    } else {
        lyricsContent[2].innerHTML = "";
    }
    if (diffs >= 3) {
        lyricsContent[3].innerHTML = lyricsData[index + 3].text;
    } else {
        lyricsContent[3].innerHTML = "";
    }
    if (diffs >= 4) {
        lyricsContent[4].innerHTML = lyricsData[index + 4].text;
    } else {
        lyricsContent[4].innerHTML = "";
    }
    if (diffs >= 5) {
        lyricsContent[5].innerHTML = lyricsData[index + 5].text;
    } else {
        lyricsContent[5].innerHTML = "";
    }
    if (diffs >= 6) {
        lyricsContent[6].innerHTML = lyricsData[index + 6].text;
    } else {
        lyricsContent[6].innerHTML = "";
    }

}

window.onkeypress = function(event) {
    if (event.which == 32) {
        if (audio.currentTime <= 0 || audio.paused == true) {
            delayedPlayPause(0, 1, 0.01, true);
        } else {
            delayedPlayPause(1, 0, 0.01, false);
        }
    }
}

playPauseButton.addEventListener("click", playPause);
card.addEventListener("dblclick", playPause);

function playPause() {

    if (audio.currentTime <= 0 || audio.paused == true) {
        // audio.volume = 1;

        playPauseButton.innerHTML = `<i style="transform: scale(1.6)" class="fa-solid fa-pause"></i>`;


        delayedPlayPause(0, 1, 0.01, true)
            // bgImg.src = `{{url_for("static",filename="/assets/icons/3.gif")}}`;
    } else {

        playPauseButton.innerHTML = `<i style="transform: scale(1.6)" class="fa-solid fa-play"></i>`;
        delayedPlayPause(1, 0, 0.01, false);
        // bgImg.src = "/music/assets/icons/4.png"
    }

}

function delayedPlayPause(i, j, k, l) {
    myloop = () => {
        setTimeout(() => {
            if (l == false) {
                i = i - k;
                if (i > j) {
                    audio.volume = i;
                    myloop();
                } else {
                    audio.pause();
                    video.pause();
                    playPauseButton.innerHTML = `<i style="transform: scale(1.6)" class="fa-solid fa-play"></i>`;
                }
            } else {
                audio.play();
                video.play();
                i = i + k;
                if (i < j) {
                    audio.volume = i;
                    myloop();
                } else {
                    playPauseButton.innerHTML = `<i style="transform: scale(1.6)" class="fa-solid fa-pause"></i>`;
                }
            }
        }, 10)
    }
    myloop();
}


progressBar.addEventListener("change", () => {
    audio.currentTime = progressBar.value * audio.duration / 100
})

//***********************swapping events***********************

swapping()

function swapping() {
    card.addEventListener('touchstart', handleTouchStart, false);
    card.addEventListener('touchmove', handleTouchMove, false);

    var xDown = null;
    var yDown = null;

    function getTouches(evt) {
        // console.log("happened")
        return evt.touches || // browser API
            evt.originalEvent.touches; // jQuery
    }

    function handleTouchStart(evt) {

        const firstTouch = getTouches(evt)[0];
        xDown = firstTouch.clientX;
        yDown = firstTouch.clientY;
    };

    function handleTouchMove(evt) {

        if (!xDown || !yDown) {

            return;
        }

        var xUp = evt.touches[0].clientX;
        var yUp = evt.touches[0].clientY;

        var xDiff = xDown - xUp;
        var yDiff = yDown - yUp;


        if (Math.abs(xDiff) > Math.abs(yDiff)) { /*most significant*/

            if (xDiff > 0) {
                /* left swipe */
            } else {
                /* right swipe */
            }
        } else {

            if (index >= 0 && index <= noOfSongs - 1) {
                //console.log("happened")
                if (yDiff > 0) {
                    //console.log(index)
                    /* up swipe */
                    let noOfSongs = songNameArr.length
                    audio.currentTime = audio.duration;

                    //console.log("swiped up")
                    if (index < noOfSongs - 1) {
                        index++;
                    } else {
                        index = 0;
                    }
                    songSelection(index)
                } else {
                    /* down swipe */
                    //console.log("swiped down")
                    let noOfSongs = songNameArr.length
                    audio.currentTime = audio.duration;

                    if (index == 0) {
                        index = noOfSongs - 1;
                        //console.log("if")
                    } else if (index <= noOfSongs - 1) {
                        index--;
                        // console.log("elseif")
                    }
                    songSelection(index)
                }
            }
        }
        /* reset values */
        xDown = null;
        yDown = null;
    };
}
//***********************swapping events***********************



// ******Buttons******
let likeBtnCount = count;
likeBtn.addEventListener("click", () => {
    if (likeBtnCount % 2 == 0) {
        likeBtn.innerHTML = `<i class="fa-solid fa-heart-circle-plus"></i>`;
        likeBtn.setAttribute("style", "color:white")
    } else {
        likeBtn.innerHTML = `<i class="fa-solid fa-heart-circle-check"></i>`;
        likeBtn.setAttribute("style", "color:red;")
    }
    likeBtnCount++;

})
let repeatBtnCount = 0;
let repeatOnceInterval;
let repeatAllInterval;
let seqAllInterval = setInterval(seqAllSong, 5000);
repeatBtn.addEventListener("click", () => {
    if (repeatBtnCount % 3 == 0) {
        repeatBtn.innerHTML = `<i class="fa-sharp fa-solid fa-repeat"></i>`;
        repeatBtn.setAttribute("style", "color:red;");
        clearInterval(repeatOnceInterval);
        shuffleBtn.setAttribute("style", "color:white;")
        clearInterval(shuffleInterval)
        clearInterval(seqAllInterval)
        repeatAllInterval = setInterval(repeatAllSong, 5000);
    } else if (repeatBtnCount % 3 == 1) {
        repeatBtn.innerHTML = `<i class="bi bi-repeat-1" style=" font-size: normal;font-weight: bolder;"></i>`;
        repeatBtn.setAttribute("style", "color:red;");
        clearInterval(repeatAllInterval);
        clearInterval(seqAllInterval)
        clearInterval(shuffleInterval)
        repeatOnceInterval = setInterval(repeatSong, 5000);
        shuffleBtn.setAttribute("style", "color:white;")

    } else {
        repeatBtn.innerHTML = `<i class="fa-sharp fa-solid fa-repeat"></i>`;
        repeatBtn.setAttribute("style", "color:white;");
        shuffleBtn.setAttribute("style", "color:white;");
        clearInterval(repeatOnceInterval);
        clearInterval(repeatAllInterval);
        clearInterval(shuffleInterval);
        seqAllInterval = setInterval(seqAllSong, 5000);
    }
    repeatBtnCount++;
    shuffleBtnCount = 0;
})
let shuffleBtnCount = 0;
let shuffleInterval;
shuffleBtn.addEventListener("click", () => {
    if (shuffleBtnCount % 2 == 0) {
        shuffleBtn.setAttribute("style", "color:red;")
        repeatBtn.setAttribute("style", "color:white;");
        clearInterval(repeatOnceInterval);
        clearInterval(repeatAllInterval);
        clearInterval(seqAllInterval)
        shuffleInterval = setInterval(shuffleSong, 5000)
    } else {
        shuffleBtn.setAttribute("style", "color:white;")
        clearInterval(shuffleInterval)
    }
    shuffleBtnCount++;
    repeatBtnCount = 0;
})

homeBtn.addEventListener("click", () => {
    searchContent.classList.add("hide");
    content.classList.remove("hide");
    homeAdder()
})

searchBtn.addEventListener("click", () => {

    title.setAttribute("style", "opacity:0")
    content.innerHTML = ``;

    $('#acc').modal('hide');
    $('#searches').modal('show');

})


accountBtn.addEventListener("click", () => {
    //title.setAttribute("style", "opacity:0");
    //console.log("clicked")
    content.innerHTML = ``;
    $('#searches').modal('hide');
    $('#acc').modal('show');

})

function homeAdder() {
    content.innerHTML = ` 
<div class="boxContainer content" id="lyricsDisplay">
    <div class="container" style=" margin-left: 10px 30px;margin-top: 10vh; ">
        <p class="lyricsContent fline" style="font-size:x-large;opacity:1;font-size:x-large;"></p>
        <p class="lyricsContent" style="font-size:small ;opacity:0.9;"></p>
        <p class="lyricsContent" style="font-size:small ;opacity:0.8;"></p>
        <p class="lyricsContent" style="font-size:small ;opacity:0.7;"></p>
        <p class="lyricsContent" style="font-size:small ; opacity:0.6;"></p>
        <p class="lyricsContent" style="font-size:small; opacity:0.5; "></p>
        <p class="lyricsContent" style="font-size:small; opacity:0.4;"></p>
    </div>
</div>`;
    title.setAttribute("style", "opacity:1")
}


// ******Buttons******
function seqAllSong() {
    let noOfSongs = songNameArr.length;
    if (audio.ended == true) {

        if (index < noOfSongs - 1) {
            index++;
            songSelection(index)
        } else {
            audio.pause();
            video.pause()
        }
    }
}

function repeatSong() {
    if (audio.ended == true) {

        songSelection(index)
    }
}


function repeatAllSong() {
    let noOfSongs = songNameArr.length
    if (audio.ended == true) {

        if (index < noOfSongs - 1) {
            index++;

        } else if (index == noOfSongs - 1) {
            index = 0;

        }

        songSelection(index)
    }
}
let counter = 0;
const shuffleArr = [];
// const shuffleArr2 = [];
let indice;
let k = 0;

function shuffleSong() {
    if (counter == 0) {
        for (let i = 0; i < noOfSongs; i++) {
            shuffleArr.push(i);
        }
        shuffleArr.sort(() => Math.random() - 0.5);
    }
    //console.log(shuffleArr.indexOf(shuffleArr[noOfSongs - 1]));

    for (key in shuffleArr) {
        if (audio.ended == true) {

            if (shuffleArr.indexOf(shuffleArr[key]) == noOfSongs - 1) {
                k = 0;
                indice = shuffleArr[k];
            } else {
                indice = shuffleArr[k++]
            }
            songSelection(indice);
        }
    }
    counter++;
}




// **********************lyrics**********************


function parseLyrics(data) {
    const regex = /^\[(?<time>\d{2}:\d{2}(.\d{2})?)\](?<text>.*)/;
    const lines = data.split('\n');
    const output = [];
    lines.forEach(element => {
        const match = element.match(regex);
        if (match == null) return;
        const { time, text } = match.groups;
        output.push({
            time: parseTime(time),
            text: text.trim()
        });

    });

    function parseTime(time) {
        let minsec = time.split(":")
        let min = parseInt(minsec[0] * 60);
        let sec = parseInt(minsec[1]);
        return min + sec;
    }
    return output;
}

function syncLyrics(lyricsData, time) {
    let differences = [];
    lyricsData.forEach(elem => {
        let diff = time - elem.time;
        if (diff >= 0) differences.push(diff);
    });
    if (differences.length == 0) return null;

    const closestLyrics = Math.min(...differences)

    return differences.indexOf(closestLyrics);

}

// **********************lyrics**********************
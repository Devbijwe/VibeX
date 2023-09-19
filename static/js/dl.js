let accContent = document.getElementById("accContent");
let searchContent = document.getElementById("searchContent")
let searchDefaultData = document.getElementById("searchDefaultData")
let dataAllSongs = document.getElementsByClassName("dataAllSongs");
let dasSongs = document.getElementsByClassName("dasSongs")
let dasArtist = document.getElementsByClassName("dasArtist");
let dasAlbum = document.getElementsByClassName("dasAlbum");
let songList = document.getElementsByClassName("songList")
let html = "";
Array.from(dasSongs).forEach((elem, index) => {
    elem.innerHTML = elem.innerHTML.replace(/_/g, " ").replace(/.mp3/i, "");
    // dasArtist[index].innerHTML = dasArtist[index].innerHTML.replace(/_/g, " ");
    // dasAlbum[index].innerHTML = dasAlbum[index].innerHTML.replace(/_/g, " ");
})


searchLoader();

function searchLoader() {

    Array.from(dataAllSongs).forEach((element, index) => {

        html += `<div class='songList'> 
        <ul class="nav pills" id="pills-tab mainList ulist" role="tablist" style="color: white;">
                    
                         
                    
        <li role="presentation" class="songli list-group-item list-group-item-action list-group-item-dark d-flex justify-content-between align-items-start">
      ${element.innerHTML}
        <a  onclick="songSelection(${index})"  class="nav-link musicLi" id="pills-home-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">
        <span class="badge playBadge" style="padding:0 10px;cursor:pointer;">
            <i style="transform: scale(1.6)" class="fa-solid fa-play"></i></span> </a>
    </li></div>
            
          `;

    });
    searchContent.innerHTML = `
    <ul class="list-group"> ${html}  
   </ul>
`;

}
$(document).ready(function() {
    $(".musicLi").click(function() {
        $(".tabNameLi").removeClass("active");
        $(".tab-pane").removeClass("active");
        $(".tabNameLi1").addClass("active");
        $(".tab-pane1").addClass("active");
    });
});

// {
//     // <a onclick="songSelection(${index})" class="list-group-item list-group-item-action  my-1 songList"  >
//     //             ${element.innerHTML}
//     //         </a>
//     /* <div class="container m-0" style="background:rgb(119, 186, 18);border:2px solid rgb(246, 5, 5)">
//     <div class="list-group my-0">

//     </div>
//     </div>  */
// }

function searching(str) {
    Array.from(dasSongs).forEach((element, index) => {

        if (element.innerHTML.toUpperCase().includes(str)) {
            songList[index].style.display = "block";
        }
        // else if (dasArtist[index].innerHTML.toUpperCase().includes(str)) {
        //     songList[index].style.display = "block";
        // } else if (dasAlbum[index].innerHTML.toUpperCase().includes(str)) {
        //     songList[index].style.display = "block";
        // }
        else {
            songList[index].style.display = "none";
        }
        // console.log(element.innerHTML.includes(str))
    });
}


let inputSearch = document.getElementById("inputSearch")
inputSearch.addEventListener("input", () => {
        str = inputSearch.value.toUpperCase();

        // console.log(str)
        searching(str);
    })
    // acc()

function acc() {
    accContent.innerHTML = `<div class="modal-header">
    <button type="button" id="closeBtn" class="btn-close" data-bs-dismiss="modal" aria-label="Close" ></button>
</div>
<div class="modal-body">
    <div class="boxContainer content" style=" padding:5px; text-align:centre; margin:auto; overflow-y:auto; overflow-x:hidden;">
        <div class="container" style=" padding:5px; text-align:centre; margin:auto; overflow-y:auto; overflow-x:hidden;">
            <form class="row g-3 my-3" action="/acc" method="post" enctype="multipart/form-data">
                <div class="col-md-6">
                <label for="inputGroupFile05" class="form-label">Song(.mp3)</label>
                    <div class="input-group">
                        <input type="file" class="form-control" id="inputGroupFile05" placeholder="songs file" name="filesongname" aria-describedby="inputGroupFileAddon05" aria-label="Upload" required>
                        
                    </div>
                </div>
                <div class="col-md-6">
                <label for="inputGroupFile04" class="form-label">Lyrics(.txt)</label>
                    <div class="input-group">
                        <input type="file" class="form-control" id="inputGroupFile04" name="filesonglyrics" aria-describedby="inputGroupFileAddon04" aria-label="Upload" required>
                       
                    </div>
                </div>
                <div class="col-md-6">
                <label for="inputStatus" class="form-label">Background Type</label>
                <select id="inputStatus" class="form-select" style="height:max-content ;" required name="bgType" placeholder="Select Background type for Song">
                <option selected value="video">Upload Video</option>
                <option  value="img"  disabled>Upload Img</option>
                <option value="ytvideo"  disabled>Add Youtube Url</option>
                </select>
            </div>
                <div class="col-md-6" id="inputType">
                <label for="inputGroupFile03" class="form-label">Background(.mp4)</label>
                <div class="input-group">
            
                    <input type="file" accept="video/mp4" class="form-control" id="inputGroupFile03" name="filesongbg" aria-describedby="inputGroupFileAddon03" aria-label="Upload" required>
                    
                
                </div>
                </div>
               
                <div class="col-12">
                    <label for="inputArtist" class="form-label">Artist</label>
                    <input type="text" class="form-control" name="artist" id="inputArtist" placeholder="Song Artists" required>
                </div>
                <div class="col-12">
                    <label for="inputAlbum" class="form-label">Album</label>
                    <input type="text" class="form-control" name="album" id="inputAlbum" placeholder="Song Album" required>
                </div>
                <div class="col-md-6">
                    <label for="inputUploadId" class="form-label">User Id</label>
                    <input type="text" class="form-control" name="userid" id="inputUploadId" placeholder="userId" required>
                </div>

                <div class="col-12">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="gridCheck" required>
                        <span><label class="form-check-label" for="gridCheck">
              Check me out
            </label></span>
                    </div>
                </div>
                <div class="col-12">
                    <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                    <button type="submit" class="btn btn-primary" style=" width:100%">Upload</button>
                </div>
            </form>
        </div>
    </div>
    <hr>
</div>
<div class="modal-footer">
    <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> 
    <button type="button" data-bs-dismiss="modal" class="btn btn-primary">Understood</button>-->
</div>`
}
// let closeBtn = document.getElementById("closeBtn");
// closeBtn.addEventListener("click", () => {
//     homeAdder()
// })

// let closeBtn2 = document.getElementById("closeBtn2");
// closeBtn2.addEventListener("click", () => {
//     homeAdder();
// });
// let inputStatus = document.getElementById("inputStatus");
// let inputType = document.getElementById("inputType")
// let html2 = ''
// inputStatus.addEventListener("change", () => {
//     if (inputStatus.value == 'img') {
//         inputType.innerHTML = `<label for="inputGroupFile03" class="form-label">Upload File</label>
//         <div class="input-group">
//             <input type="file" accept="image/*" class="form-control" id="inputGroupFile03" name="filesongbg" aria-describedby="inputGroupFileAddon03" aria-label="Upload" required>
//             <button class="btn btn-outline-secondary" type="button" id="inputGroupFileAddon03">Background Img</button>
//         </div>`;
//     } else if (inputStatus.value == 'video') {
//         inputType.innerHTML = `<label for="inputGroupFile03" class="form-label">Upload File</label>
//                     <div class="input-group">
//                         <input type="file" accept="video/mp4" class="form-control" id="inputGroupFile03" name="filesongbg" aria-describedby="inputGroupFileAddon03" aria-label="Upload" required>
//                         <button class="btn btn-outline-secondary" type="button" id="inputGroupFileAddon03">Background Video</button>
//                     </div>`;
//     } else if (inputStatus.value == 'ytvideo') {
//         inputType.innerHTML = `<label for="inputGroupFile03" class="form-label">Upload File</label>
//         <div class="input-group">
//             <input type="url" name="filesongbg"  class="form-control" id="inputGroupFile03" aria-describedby="inputGroupFileAddon03" aria-label="Upload" required>
//         </div>`;
//     }
//     console.log(inputStatus.value)
// });
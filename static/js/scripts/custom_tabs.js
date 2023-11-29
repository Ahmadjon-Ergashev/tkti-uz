const tab_btns = document.querySelectorAll("#events .tab_btn");
const content = document.querySelectorAll("#events .content");
tab_btns.forEach((tab, index) => {
    tab.addEventListener("click", (e)=>{
        tab_btns.forEach(tab=>{tab.classList.remove("active_tap")})
        tab.classList.add("active_tap")
        var line = document.querySelector(".line");
        line.style.width = e.target.offsetWidth + "px";
        line.style.left = e.target.offsetLeft + "px";
        content.forEach((content)=>{content.classList.remove("d-block")})
        content[index].classList.add("d-block")
    })
})
const news_tab_btns = document.querySelectorAll("#news_ads_videos .tab_btn");
const news_content = document.querySelectorAll("#news_ads_videos .content");
news_tab_btns.forEach((tab, index) => {
    tab.addEventListener("click", (e)=>{
        news_tab_btns.forEach(tab=>{tab.classList.remove("active_tap")})
        tab.classList.add("active_tap")
        var line = document.querySelector(".line");
        line.style.width = e.target.offsetWidth + "px";
        line.style.left = e.target.offsetLeft + "px";
        news_content.forEach((news_content)=>{news_content.classList.remove("d-block")})
        news_content[index].classList.add("d-block")
    })
})

const sem_tab_btns = document.querySelectorAll("#module_by_semesters .tab_btn");
const sem_content = document.querySelectorAll("#module_by_semesters .content");
sem_tab_btns.forEach((tab, index) => {
    tab.addEventListener("click", (e)=>{
        sem_tab_btns.forEach(tab=>{tab.classList.remove("active_tap")})
        tab.classList.add("active_tap")
        sem_content.forEach((sem_content)=>{sem_content.classList.remove("d-block")})
        sem_content[index].classList.add("d-block")
    })
})


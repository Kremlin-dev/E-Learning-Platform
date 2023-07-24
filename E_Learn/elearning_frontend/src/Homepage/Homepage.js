// Navbar responsiveness
const toggleBtn = document.querySelector('.app__header-menu');
const toggleBtnIcon = document.querySelector('.app__header-menu i');
const smallscreenMenu = document.querySelector('.app__header-smallscreen_menu');


toggleBtn.onclick =  function(){
    smallscreenMenu.classList.toggle('open');

    const isOpen =  smallscreenMenu.classList.contains('open');
    toggleBtnIcon.classList = isOpen ? "fa fa-times" : "fa fa-bars";
}


// change bgcolor on scroll

function changeBag(){
 var navbar = document.getElementById('navbar');
 var scrollWindow = window.scrollY;
 if(scrollWindow > 30){
    navbar.classList.add('changeBg')
 }
 else{
    navbar.classList.remove('changeBg')
 }
 }

window.addEventListener('scroll', changeBag)

// Aos initialisation
AOS.init({
	duration: 1200,
});




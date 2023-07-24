'use strict';

let navIcons = document.querySelectorAll(".nav-icons");

let conBody = document.getElementById("container-body");
let editProfile = document.getElementById("edit-profile");
let resetPassword = document.getElementById("reset-password");
let uploadVideo = document.getElementById("upload-video");




const handleClick = (event) => {
   
    switch(event.target.innerText)
    {
        case "Profile":
            {
               // console.log("Profile clicked");
                if(conBody.style.display ='none')
                {
                    conBody.style.display ='flex';
                    // conBody.innerText.style.color = ' #41f1f1';
                    editProfile.style.display = 'none';
                    resetPassword.style.display = 'none';
                    uploadVideo.style.display = 'none';

                }
            }
        break;

        case "Edit Profile":
            {
                editProfile.style.display = 'block';
                // editProfile.innerText.style.color = ' #41f1f1';
                conBody.style.display = 'none';
                resetPassword.style.display = 'none';
                uploadVideo.style.display = 'none';
                
            }

        break;

        case "Change Password":
            {
                resetPassword.style.display = 'block';
                conBody.style.display = 'none';
                editProfile.style.display = 'none';
                uploadVideo.style.display = 'none';
            }
        break;

        }
  };

navIcons.forEach(element => {
    
    element.addEventListener('click', handleClick);
    
    
});

let activeButton = document.getElementById('profilebtn');

// Add event listeners to each button
navIcons.forEach((button) => {
  button.addEventListener('click', function () {
    if (this === activeButton) {
      this.style.color = '#06c4c4'; // Toggle back to the original color
    } else {
      activeButton.style.color = 'black'; // Reset the text color of the previously active button
      this.style.color = '#06c4c4'; // Set the text color of the clicked button
      activeButton = this; // Set the current button as the active button
    }
  });
});

const year = document.getElementById('year');
const currentYear = new Date().getFullYear();
year.textContent = currentYear;














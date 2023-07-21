'use strict';

// dummydata for courses
const courses = [
    {
      id:1,
      thumbnail : '../assets/css.avif',
      videoName : "Introduction to Css",
      video : '../assets/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
    },

    {
      id:2,
      thumbnail : '../assets/c++.png',
      videoName : "Learn C++ Programming",
      video : '../assets/allison.mp4',
      description: "C++ is an object-oriented programming language which gives a clear structure to programs and allows code to be reused, lowering development costs",
    },
    {
      id:3,
      thumbnail : '../assets/html.png',
      videoName : "Introduction to html",
      video : '../assets/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
      
    },
    {
      id:4,
      thumbnail : '../assets/Java.png',
      videoName : "Introduction to java",
      video : '../assets/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
      
    },
    {
      id:5,
      thumbnail : '../assets/javascript.jpg',
      videoName : "Introduction to javascript",
      video : '../assets/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
     
    },
    {
      id:6,
      thumbnail : '../assets/php.png',
      videoName : "Introduction to php",
      video : '../assets/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
      
    },
    {
      id:7,
      thumbnail : '../assets/python.png',
      videoName : "Introduction to python",
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
    },
    {
      id:8,
      thumbnail : '../assets/c++.png',
      videoName : "Introduction to Css",
      video : '../assets/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
      
    },
]

const videoContainer = document.querySelector('.video-container');
const searchInput = document.querySelector('.search-bar');
const buttons = document.querySelectorAll('.links');let searchTerm = searchInput.value.toLowerCase();

courses.map((item) =>{
    videoContainer.innerHTML += `
    <div class="video">
    <img src=${item.thumbnail} class="thumbnail" alt="">
    <div class="video-content">
     <h5 class="font-bold">${item.videoName}</h5>
     <p class="text-sm mt-2 mb-2">${item.description}</p>
    </div>
    </div> 
    `})
 
    // search button functionality
searchInput.addEventListener('keypress', performSearch); 

function performSearch() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const videoContainer = document.querySelector('.video-container');

    // Clear previous search results
    videoContainer.innerHTML = '';
    let searchTerm = '';

   
        if (this.tagName === 'A') {
            searchTerm = this.dataset.searchTerm.toLowerCase();
          } else {
            searchTerm = searchInput;
          }

          const matchingCourses = courses.filter(course =>
            course.videoName.toLowerCase().includes(searchTerm)
            );
console.log(searchTerm);

    if (matchingCourses.length > 0) {
    
      matchingCourses.map((item) =>{
        videoContainer.innerHTML += `
        <div class="video">
        <img src=${item.thumbnail} class="thumbnail" alt="">
        <div class="video-content">
         <h5 class="font-bold">${item.videoName}</h5>
         <p class="text-sm mt-2 mb-2">${item.description}</p>
        </div>
        </div> 
        `
      })
      
    } else {
      const noResultsItem = document.createElement('div');
      noResultsItem.innerHTML = '<div id = "no-results">No results found. </div>';
      videoContainer.appendChild(noResultsItem);
    }
  }

  function handleKeyPress(event) {
    // Check if the key pressed is the space bar or enter key
    if (event.keyCode === 32 || event.keyCode === 13) {
      performSearch();
    }
  }

  // Event listener for search button click
  document.querySelector('.search-btn').addEventListener('click', performSearch);

//   Event listener for key press in the input field
  document.getElementById('searchInput').addEventListener('keydown', handleKeyPress);

  buttons.forEach(button => {
    button.addEventListener('click', performSearch);
  });
  

  
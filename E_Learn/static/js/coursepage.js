'use strict';

// dummydata for courses
const courses = [
    {
      id:1,
      thumbnail : '../static/images/css.avif',
      videoName : "Introduction to Css",
      video : '../static/images/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
    },

    {
      id:2,
      thumbnail : '../static/images/c++.png',
      videoName : "Learn C++ Programming",
      video : '../static/images/allison.mp4',
      description: "C++ is an object-oriented programming language which gives a clear structure to programs and allows code to be reused, lowering development costs",
    },
    {
      id:3,
      thumbnail : '../static/images/html.png',
      videoName : "Introduction to html",
      video : '../static/images/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
      
    },
    {
      id:4,
      thumbnail : '../static/images/Java.png',
      videoName : "Introduction to java",
      video : '../static/images/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
      
    },
    {
      id:5,
      thumbnail : '../static/images/javascript.jpg',
      videoName : "Introduction to javascript",
      video : '../static/images/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
     
    },
    {
      id:6,
      thumbnail : '../static/images/php.png',
      videoName : "Introduction to php",
      video : '../static/images/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
      
    },
    {
      id:7,
      thumbnail : '../static/images/python.png',
      videoName : "Introduction to python",
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
    },
    {
      id:8,
      thumbnail : '../static/images/c++.png',
      videoName : "Introduction to Css",
      video : '../static/images/allison.mp4',
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
  

  
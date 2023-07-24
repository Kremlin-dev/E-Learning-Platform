// Define the courses array with the course data
const courses = [
    {
      id: 1,
      thumbnail: '../static/images/css.avif',
      videoName: "Introduction to Css",
      video: '../static/images/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
    },
    {
      id: 2,
      thumbnail: '../static/images/c++.png',
      videoName: "Learn C++ Programming",
      video: '../static/images/allison.mp4',
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

    
    
  ];
  
  // Function to render courses in the video container
  function renderCourses(courses) {
    const videoContainer = document.querySelector('.video-container');
    const videoLinks = document.querySelectorAll('.video-link');

    videoContainer.innerHTML = '';
  
    courses.map((item) => {
      videoContainer.innerHTML += `
      <div class="video">
      <img src=${item.thumbnail} class="thumbnail" alt="">
      <div class="video-content">
        <h5 class="font-bold">
          <a href="#" data-course-id="${item.id}" class="video-link">${item.videoName}</a>
        </h5>
        <p class="text-sm mt-2 mb-2">${item.description}</p>
      </div>
      </div> 
      `;
    });
  
    // Add event listener to the video links
       videoLinks.forEach(link => {
       link.addEventListener('click', redirectToVideo);
    });
  }
  
  function redirectToVideo(event) {
    event.preventDefault();
    const courseId = event.target.dataset.courseId;
    const course = courses.find(item => item.id.toString() === courseId);
    if (course) {
      // Construct the video URL with the courseId
      const videoUrl = `/play_video/${courseId}`;
  
      // Make a GET request to the Flask route to retrieve the video
      fetch(videoUrl)
        .then(response => {
          if (!response.ok) {
            throw new Error('Video not found');
          }
          return response.blob();
        })
        .then(videoBlob => {
          // Create a URL object for the video blob and redirect to it
          const videoObjectUrl = URL.createObjectURL(videoBlob);
          window.location.href = videoObjectUrl;
        })
        .catch(error => {
          console.error(error);
          alert('Video not found');
        });
    } else {
      console.error('Course not found!');
    }
  }
  

  // Function to perform search based on user input
  function performSearch() {
    const videoContainer = document.querySelector('.video-container');
    var searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput.value.toLowerCase();
    const links = document.getElementsByClassName('links');

    const matchingCourses = courses.filter(course =>
    course.videoName.toLowerCase().includes(searchTerm));
     renderCourses(matchingCourses);
   
    //  // Clear previous search results
     videoContainer.innerHTML = '';
     searchInput = '';

        
        const sidebarTerm = links.dataset.searchData.toLowerCase();
        const newMarch = courses.filter(newcourse => newcourse.videoName.toLowerCase())
        if(newMarch.includes(sidebarTerm)) {
          renderCourses(newMarch);
        }
       

      if(matchingCourses === 0) {
       const noResultsItem = document.getElementById('no-results');
       noResultsItem.innerHTML = 'No results found';   
     }
    
       
  }
  
  // Function to handle key press in the input field
  function handleKeyPress(event) {
    // Check if the key pressed is the space bar or enter key
    if (event.keyCode === 32 || event.keyCode === 13) {
      performSearch();
    }
  }
  
  // Event listener for search button click
  document.querySelector('.search-btn').addEventListener('click', performSearch);
  
  // Event listener for key press in the input field
  document.getElementById('searchInput').addEventListener('keydown', handleKeyPress);
  
  // Event listener for links in the sidebar
  const links = document.querySelectorAll('.links');
  links.forEach(button => {
    button.addEventListener('click', performSearch);
  });
  
  // Initial rendering of courses
  renderCourses(courses);
  
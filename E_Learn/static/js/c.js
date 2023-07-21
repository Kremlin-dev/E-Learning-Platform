// Define the courses array with the course data
const courses = [
    {
      id: 7,
      thumbnail: '../static/images/css.avif',
      videoName: "Introduction to Css",
      video: '../static/images/allison.mp4',
      description: "Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML.",
    },
    {
      id: 6,
      thumbnail: '../static/images/c++.png',
      videoName: "Learn C++ Programming",
      video: '../static/images/allison.mp4',
      description: "C++ is an object-oriented programming language which gives a clear structure to programs and allows code to be reused, lowering development costs",
    },
    // Add other course objects as needed...
  ];
  
  // Function to render courses in the video container
  function renderCourses(courses) {
    const videoContainer = document.querySelector('.video-container');
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
    const videoLinks = document.querySelectorAll('.video-link');
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
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const matchingCourses = courses.filter(course =>
      course.videoName.toLowerCase().includes(searchInput)
    );
  
    renderCourses(matchingCourses);
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
  const buttons = document.querySelectorAll('.links');
  buttons.forEach(button => {
    button.addEventListener('click', performSearch);
  });
  
  // Initial rendering of courses
  renderCourses(courses);
  
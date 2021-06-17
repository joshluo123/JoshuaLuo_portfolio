// Author: Joshua Luo
// Date: 11/23/2020
// Description: CS 290 section 400: Project

var apiKey = "RGAPI-393680d6-3c4c-49df-813a-b9774bba41d3";

var currCarouselIndex = 0;
var carouselItems = [];
carouselItems.push(document.getElementById("carouselItem0"));
carouselItems.push(document.getElementById("carouselItem1"));
carouselItems.push(document.getElementById("carouselItem2"));
carouselItems.push(document.getElementById("carouselItem3"));
carouselItems.push(document.getElementById("carouselItem4"));

document.addEventListener("DOMContentLoaded", bindButtons);
document.addEventListener("DOMContentLoaded", function() {
	carouselItems[currCarouselIndex].style.visibility = "visible";
	});

var autoRot = setInterval(autoRotateCarousel, 3000);

function bindButtons() {
	document.getElementById("carouselButtonPrev").addEventListener("click", function(event){
		clearInterval(autoRot);
		carouselItems[currCarouselIndex].style.display = "none";
		if (currCarouselIndex == 0) {
			currCarouselIndex = carouselItems.length - 1;
		} else {
			currCarouselIndex -= 1;
		}
		carouselItems[currCarouselIndex].style.display = "block";

		autoRot = setInterval(autoRotateCarousel, 3000);
		event.stopPropagation();
	});

	document.getElementById("carouselButtonNext").addEventListener("click", function(event){
		clearInterval(autoRot);
		carouselItems[currCarouselIndex].style.display = "none";

		if (currCarouselIndex == carouselItems.length - 1) {
			currCarouselIndex = 0;
		} else {
			currCarouselIndex += 1;
		}

		carouselItems[currCarouselIndex].style.display = "block";

		autoRot = setInterval(autoRotateCarousel, 3000);
		event.stopPropagation();
	});
}

function autoRotateCarousel() {
	carouselItems[currCarouselIndex].style.display = "none";
		if (currCarouselIndex == carouselItems.length - 1) {
			currCarouselIndex = 0;
		} else {
			currCarouselIndex += 1;
		}
		carouselItems[currCarouselIndex].style.display = "block";
}
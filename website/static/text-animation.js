const t1 = gsap.timeline({ defaults: {ease: "power1.out"} });


if(window.location.pathname == "/index.php"){
	t1.to(".intro", {y: "-100%", duration: .75, delay: 1});
	t1.to(".slider", {y: "-100%", duration: 1}, "-=.75");
	t1.fromTo(".navbar", {opacity: 0}, {opacity: 1, duration: 1});
	t1.fromTo(".white-text-large", {opacity: 0}, {opacity: 1, duration: 1}, "-=1");
	t1.fromTo(".white-text", {opacity: 0}, {opacity: 1, duration: 1}, "-=1");
}


gsap.registerPlugin(ScrollTrigger);

gsap.from(".animate-left", {
	scrollTrigger: ".animate-left",
	x: 300,
	duration: 2,
	opacity:0
});

gsap.from(".animate-up", {
	scrollTrigger: ".animate-up",
	y: 200,
	duration: 2,
	opacity:0
});

gsap.from(".animate-right", {
	scrollTrigger: ".animate-right",
	x: -300,
	duration: 2,
	opacity:0
});

gsap.from(".animate-up-wr", {
	scrollTrigger: ".animate-right",
	y: 200,
	duration: 2,
	opacity:0
});

gsap.from(".animate-up-wl", {
	scrollTrigger: ".animate-left",
	y: 200,
	duration: 2,
	opacity:0
});

gsap.from(".animate-up-wl2", {
	scrollTrigger: ".animate-left2",
	y: 200,
	duration: 2,
	opacity:0
});

gsap.from(".animate-left2", {
	scrollTrigger: ".animate-left2",
	x: 300,
	duration: 2,
	opacity:0
});

gsap.from(".animate-up2", {
	scrollTrigger: ".animate-up2",
	y: 200,
	duration: 2,
	opacity:0
});

gsap.from(".animate-up3", {
	scrollTrigger: ".animate-up3",
	y: 200,
	duration: 2,
	opacity:0
});

gsap.from(".animate-fadein5", {
	scrollTrigger: ".animate-fadein5",
	duration: 5,
	opacity:0
});

//Our Team Page
var cards = document.getElementsByClassName("a-card");
for(var i = 0; i < cards.length; i++){
	gsap.from(cards.item(i), {
		scrollTrigger: cards.item(i),
		duration: 3,
		opacity:0
	});
}

//Our Team Page
var section = document.getElementsByClassName("list");
var list = section.getElementsByTagName("li");
for(var i = 0; i < list.length; i++){
	gsap.from(list.item(i), {
		scrollTrigger: list.item(i),
		duration: 2,
		opacity:0,
		y:100
	});
}


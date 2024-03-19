const t1 = gsap.timeline({ defaults: {ease: "power1.out"} });

gsap.registerPlugin(ScrollTrigger);

gsap.from(".animate-left", {
	scrollTrigger: ".animate-left",
	x: 300,
	duration: 0.7,
	opacity:0
});

gsap.from(".animate-up", {
	scrollTrigger: ".animate-down",
	y: 100,
	duration: 1,
	opacity:0.2
});
gsap.from(".animate-down", {
	scrollTrigger: ".animate-down",
	y: -100,
	duration: 1.2,
	opacity:0
});

gsap.from(".animate-right", {
	scrollTrigger: ".animate-right",
	x: -300,
	duration: 0.7,
	opacity:0
});

gsap.from(".animate-up-wr", {
	scrollTrigger: ".animate-right",
	y: 200,
	duration: 0.7,
	opacity:0
});

gsap.from(".animate-up-wl", {
	scrollTrigger: ".animate-left",
	y: 200,
	duration: 0.7,
	opacity:0
});

gsap.from(".animate-up-wl2", {
	scrollTrigger: ".animate-left2",
	y: 200,
	duration: 0.7,
	opacity:0
});

gsap.from(".animate-left2", {
	scrollTrigger: ".animate-left2",
	x: 300,
	duration: 0.7,
	opacity:0
});

gsap.from(".animate-up2", {
	scrollTrigger: ".animate-up2",
	y: 200,
	duration: 0.7,
	opacity:0
});

gsap.from(".animate-up3", {
	scrollTrigger: ".animate-up3",
	y: 200,
	duration: 0.7,
	opacity:0
});

gsap.from(".animate-fadein5", {
	scrollTrigger: ".animate-fadein5",
	duration: 0.7,
	opacity:0
});

//Our Team Page
var cards = document.getElementsByClassName("a-card");
for(var i = 0; i < cards.length; i++){
	gsap.from(cards.item(i), {
		scrollTrigger: cards.item(i),
		duration: 0.7,
		opacity:0
	});
}


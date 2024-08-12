import authorProfileImage from "../assets/alan-profile.JPG"

function About() {
    return (
        <>
            <style>
                {`
                    p {
                        line-height: 2;
                        font-size: 1.2em;
                    }
                `}
            </style>
            <div className="max-w-[1200px] mx-auto w-full pb-10 md:pb-20 pt-20 px-10 box-content">
                <h1 className="text-3xl lg:text-5xl font-semibold py-20 md:pt-40">About</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                    <div>
                        <img src={authorProfileImage} alt="Alan Thomas profile picture" className="w-full h-full object-cover rounded-xl shadow-custom" />
                    </div>
                    <div>
                        <h2 className="text-xl lg:text-3xl font-semibold italic pb-6">Hi, I’m Alan! Web Development and Media Design Instructor.</h2>
                        <p className="font-extralight">
                            With a Bachelor's degree in Computer Science from Simon Fraser University, I have built a diverse and impactful career in the tech industry.
                            My journey began as a <span className="font-bold italic">Frontend Developer</span> intern, where I honed my skills in creating intuitive user interfaces and enhanced user experiences.
                            Over the course of a year, I transitioned into roles as a <span className="font-bold italic">Software Development Engineer in Test (SDET)</span> and a <span className="font-bold italic">Software Engineer</span>, contributing nearly three years of expertise to the industry.
                            <br />
                            <br />
                            My passion for technology and education led me to my current role as an <span className="font-bold italic">Instructor in the New Media Design and Web Development</span> program at BCIT.
                            Here, I have the privilege of shaping the next generation of developers by combining my industry experience with a deep commitment to <span className="font-bold italic">innovative and student-centered teaching</span>.
                            <br />
                            <br />
                            I am driven by the belief that technology can create meaningful change and am dedicated to building solutions that are both functional and impactful.
                            My career is rooted in <span className="font-bold italic">continuous learning, collaboration,</span> and a commitment to fostering an <span className="font-bold italic">inclusive and equitable digital future</span>.
                        </p>
                    </div>
                </div>
            </div>
        </>
    )
}

export default About;
import { Helix } from 'ldrs/react';
import 'ldrs/react/Helix.css';


function Spinner() {
    return (
        <>
            <div className="w-full h-[60vh] content-center text-center">
                <Helix
                    size="150"
                    speed="2.5"
                    color="white" 
                />
            </div>
        </>
    )
}

export default Spinner;
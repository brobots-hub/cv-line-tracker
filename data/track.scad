radius = 5;
straigth_length = 15;
width = 0.5;
height = 0.0001;

module track() {
    scale([straigth_length,width,height])
    square(size=1, center=true);

    scale([width,straigth_length,height])
    square(size=1, center=true);

    module round_track() {
        difference() {
            
            translate([straigth_length/2-width/2, straigth_length/2-width/2, 0])
            scale([1,1,height])
            circle(r=straigth_length/2, $fn=300);
            
            translate([straigth_length/2-width/2, straigth_length/2-width/2, 0])
            scale([1,1,height*2])
            circle(r=straigth_length/2-width, $fn=300);
            
            scale([1,1,height*2])
                    square(straigth_length, center=true);
        }
    }

    round_track();

    rotate([0,0,180])
    round_track();
}

//projection(cut=false) translate([0,0,0])
track();
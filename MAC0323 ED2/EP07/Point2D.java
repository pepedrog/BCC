
import java.lang.IllegalArgumentException;

public class Point2D implements Comparable<Point2D> {

	private double x, y;
    // construct the point (x, y)
    public Point2D(double x, double y){
		this.x = x;
		this.y = y;
	}

    // x-coordinate 
    public double x(){
		return this.x;
	}

    // y-coordinate 
    public double y(){
		return this.y;
	}

    // square of Euclidean distance between two points 
    public double distanceSquaredTo(Point2D that){
		double a = this.x - that.x();
		double b = this.y - that.y();
		return (a*a + b*b);
	}

    // for use in an ordered symbol table 
    public int compareTo(Point2D that)

    // does this point equal that object? 
    public boolean equals(Object that){
		if(that.type != Point2D) throw new IllegalArgumentException();
		return (this.x() == that.x && this.y == that.y());
	}

    // string representation 
    public String toString(){
		return ( "(" + this.x.toString() + " " + this.y.toString() + ")");
	}

}
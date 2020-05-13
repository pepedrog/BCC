/* *****************************************************************************
 *  Compilation:  javac SolverVisualizer.java
 *  Execution:    java SolverVisualizer filename
 *  Dependencies: Solver.java Board.java
 *
 *  This program takes the name of a file as a command-line argument.
 *  From that file, it
 *
 *    - Uses your Solver.java and Board.java programs to solve the
 *      sliding block puzzle defined by the input file.
 *    - Renders a graphical animation of your program's output.
 *    - Uses the manhattan() method in Board to display the
 *      Manhattan distance at each stage of the solution. 
 *
 *  by Martin Round. September 2014 Coursera Algorithms, Part I course
 *
 *  % java SolverVisualizer puzzle07.txt
 *
 **************************************************************************** */

import java.awt.Color;
import java.awt.Font;

import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

public class SolverVisualizer {

    // time in milliseconds to animate each move of the solution
    private static final int ANIMATE_TIME = 800;

    // time in milliseconds to pause after each move
    private static final int PAUSE_TIME = 300;

    // time in milliseconds for each frame of animation. 20 is sensible
    private static final int FRAME_TIME = 20;

    // background color of tile
    private static final Color TILE_BACKGROUND_COLOR = Color.WHITE;

    // foreground color of tile
    private static final Color TILE_FOREGROUND_COLOR = Color.BLACK;

    // background color of board
    private static final Color BOARD_COLOR = Color.LIGHT_GRAY;

    // text color
    private static final Color TEXT_COLOR = Color.BLACK;
    
    private static int n;            // dimension of grid
    private static int[][] tileAt;   // number of tile at [row][column]
    private static int movingTile;   // which tile is moving, or 0 if none
    private static int totalMoves;   // number of moves to solve puzzle
    private static int currentMoves; // number of moves currently displayed
    private static int manhattan;    // Manhattan distance currently displayed
    private static String title;
    
    // Draw one frame of animation.
    // If the start position is being displayed (movingTile == 0) or during
    // the PAUSE_TIME following each animated move, the display is unchanged.
    // moveTime is the number of milliseconds since the current move began.
    private static void refresh(int moveTime) {
        // find where the empty space (0 tile) is located
        int emptyRow = 0;
        int emptyCol = 0;
        while (tileAt[emptyRow][emptyCol] != 0) {
            if (++emptyCol == n) {
                emptyCol = 0;
                ++emptyRow;
            }
        }

        StdDraw.clear();
        StdDraw.setPenColor(StdDraw.BLACK);
        StdDraw.setXscale(-0.1*n, 1.1*n);
        StdDraw.setYscale(-0.1*n, 1.1*n);
        StdDraw.setPenRadius(0.03 / n);
        int fontSize = 200 / n;
        StdDraw.setFont(new Font("SansSerif", Font.PLAIN, fontSize));

        StdDraw.setPenColor(BOARD_COLOR);
        StdDraw.filledSquare(n/2.0, n/2.0, n/1.96);
   
        for (int row = 0; row < n; row++) {
            for (int col = 0; col < n; col++) {
                double x = col + 0.5;
                double y = n - row - 0.5;
                if (tileAt[row][col] == movingTile) {
                    double moveFraction = (double) moveTime / ANIMATE_TIME;
                    if (moveFraction > 1.0) moveFraction = 1.0;
                    x += (1.0 - moveFraction) * (emptyCol - col);
                    y -= (1.0 - moveFraction) * (emptyRow - row);
                }
                if (tileAt[row][col] != 0) {
                    StdDraw.setPenColor(TILE_BACKGROUND_COLOR);
                    StdDraw.filledSquare(x, y, 0.475);
                    StdDraw.setPenColor(TILE_FOREGROUND_COLOR);
                    StdDraw.square(x, y, 0.475);
                    StdDraw.text(x, y - 0.05, "" + tileAt[row][col]);
                }
            }
        }

        // write status text
        StdDraw.setFont(new Font("SansSerif", Font.PLAIN, 12));
        StdDraw.setPenColor(TEXT_COLOR);
        StdDraw.text(0.100 * n, -0.06 * n, currentMoves + "/" + totalMoves + " moves");
        StdDraw.text(0.775 * n, -0.06 * n, "Manhattan distance: " + manhattan);
        StdDraw.text(0.500 * n,  1.06 * n, title);
    }
    
    private static void animateMove() {
        int milliseconds = 0;
        while (milliseconds < ANIMATE_TIME + PAUSE_TIME) {
            refresh(milliseconds);
            StdDraw.show();
            StdDraw.pause(FRAME_TIME);
            milliseconds += FRAME_TIME;
        }   
    }
    
    public static void main(String[] args) {
        StdDraw.enableDoubleBuffering();

        // for each command-line argument
        for (String filename : args) {

            // read in the board specified in the filename
            In in = new In(filename);
            n = in.readInt();
            tileAt = new int[n][n];
            for (int row = 0; row < n; row++) {
                for (int col = 0; col < n; col++) {
                    tileAt[row][col] = in.readInt();
                }
            }
            
            title = filename;
            movingTile = 0; // show initial state for first 'move time'
            
            // solve the slider puzzle
            Board initial = new Board(tileAt);
            manhattan = initial.manhattan();
            
            long start = System.currentTimeMillis();
            
            if (!initial.isSolvable()) {
                long now = System.currentTimeMillis();
                title += " (no solution possible)";
                movingTile = 0;
                currentMoves = 0;
                animateMove(); // display start position only
            }
            else {
                Solver solver = new Solver(initial);
                totalMoves = solver.moves();
                currentMoves = 0;

                for (Board board : solver.solution()) {
                    manhattan = board.manhattan();
                    for (int row = 0; row < n; row++) {
                        for (int col = 0; col < n; col++) {
                            int tile = board.tileAt(row, col);
                            // if this position was previously empty
                            if (tileAt[row][col] == 0)
                                movingTile = tile; // animate the tile into it
                            tileAt[row][col] = tile;
                        }
                    }
                    animateMove(); // show move (or static initial state 1st time)
                    currentMoves++;
                }
                // show final position for one extra 'move time' before (possibly)
                // moving on to display next puzzle solution.
                StdDraw.show();
                StdDraw.pause(ANIMATE_TIME + PAUSE_TIME);
            }
            StdOut.println(title);
        }            
    }
}

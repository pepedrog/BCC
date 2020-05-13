import algs4.edu.princeton.cs.algs4.WeightedQuickUnionUF;
import algs4.edu.princeton.cs.algs4.StdOut;
public class Percolation {

    private WeightedQuickUnionUF grid;
    private int n, n_open;
    private boolean[] grid_open;
    private int virtual_top, virtual_bottom;
    // creates n-by-n grid, with all sites initially blocked
    public Percolation(int n){
      int sz = n*n;
      virtual_top = sz;
      virtual_bottom = sz + 1;
      grid = WeightedQuickUnionUF(sz + 2);
      this.n = n;
      for(int i = 0; i < n; i++){
        grid.join(i, virtual_top);
        grid.join(sz - 1 - i, virtual_bottom + 1);
      }
      grid_open = new boolean[sz];
      n_open = 0;

    }

    // opens the site (row, col) if it is not open already
    public void open(int row, int col){
      if(!isValid(row, col)) throw new IllegalArgumentException();
      int pos = index(row, col);
      int directions[][] = {{row + 1, col}, {row - 1, col}, {pos, col + 1}, {pos, col - 1}};

      if(!grid_open[pos]){
         n_open++;
         grid_open[pos] = true;

         for(int i = 0; i < 4; i++){
           if(isValid(directions[i][0], directions[i][1]) && isOpen(directions[i][0], directions[i][1])) grid.union(pos, index(directions[i][0], directions[i][1]));
         }
       }
    }

    // is the site (row, col) open?
    public boolean isOpen(int row, int col){
      if(!isValid(row, col)) throw new IllegalArgumentException();
      return grid_open[index(row, col)];
    }

    // is the site (row, col) full?
    public boolean isFull(int row, int col){
      if(!isValid(row, col)) throw new IllegalArgumentException();
      return grid.connected(index(row, col), virtual_top);
    }

    // returns the number of open sites
    public int numberOfOpenSites(){
      return n_open;
    }

    // does the system percolate?
    public boolean percolates(){
      return(grid.connected(virtual_top, virtual_bottom));
    }

    // unit testing (required)
    public static void main(String[] args){
      StdOut.println("começando os testes");
    }

    private int index(int row, int col){
      return (row*n + col);
    }

    private boolean isValid(int row, int col){
      return (row < n && col < n && row >=0 && col >= 0);
    }

}
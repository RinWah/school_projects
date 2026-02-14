public class clamp {
    public static int clamp(int x, int min, int max) {
        if (min > max) throw new IllegalArgumentException("min > max");
        if (x < min) return min;
        if (x > max) return max;
        return x;
    }
}

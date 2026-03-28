import java.util.Random;

public class Fuzzer {
    private static final String ALPHA = "abcdefghijklmnopqrstuvwxyz";
    private static final Random RAND = new Random();
    public static String generateRandomInput() {
        // "slots" for words/spaces
        int iterations = RAND.nextInt(10) + 1;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < iterations; i++) {
            // add leading spaces / spaces between words
            int spaceCount = RAND.nextInt(4); // 0-3 spaces
            for (int s = 0; s < spaceCount; s++) {
                sb.append(" ");
            }
            // ranndom word
            int wordLength = RAND.nextInt(8); // 0-7 chars
            for (int c = 0; c < wordLength; c++) {
                sb.append(ALPHA.charAt(RAND.nextInt(ALPHA.length())));
            }
        }
        // trailing spaces
        if (RAND.nextBoolean()) {
            sb.append("  ");
        }
        return sb.toString();
    }
}

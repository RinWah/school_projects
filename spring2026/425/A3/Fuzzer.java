import java.util.Random;

public class Fuzzer {
    private static final String ALPHA = "abcdefghijklmnopqrstuvwxyz";
    private static final Random RAND = new Random();
    // professor's method to be tested 
    public static String reverseAndCapWords(String input) {
        // validation block 
        if (input == null || input.isEmpty()) {
            throw new IllegalArgumentException("input cannot be null or empty.");
        }
        
        String[] words = input.split(" "); 
        StringBuilder reversedString = new StringBuilder();
        
        // looping backwards 
        for (int i = words.length - 1; i >= 0; i--) {
            // landmine: substring(0, 1) on an empty string causes a crash 
            String cap = words[i].substring(0, 1).toUpperCase() + words[i].substring(1);
            reversedString.append(cap).append(" ");
        }
        
        String result = reversedString.toString().trim(); // [cite: 15]
        return result;
    }
    // your random fuzzer logic 
    public static String generateRandomInput() {
        int iterations = RAND.nextInt(10) + 1;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < iterations; i++) {
            int spaceCount = RAND.nextInt(4); 
            for (int s = 0; s < spaceCount; s++) {
                sb.append(" ");
            }
            int wordLength = RAND.nextInt(8); 
            for (int c = 0; c < wordLength; c++) {
                sb.append(ALPHA.charAt(RAND.nextInt(ALPHA.length())));
            }
        }
        if (RAND.nextBoolean()) {
            sb.append(" ");
        }
        return sb.toString();
    }
    // mutation op 1: delete random char
    public static String deleteMutation(String s) {
        if (s.length() == 0) return s;
        int index = RAND.nextInt(s.length());
        return s.substring(0, index) + s.substring(index + 1);
    }
    public static void runMutationFuzzer() {
        String[] seeds = {"this is a test string", "fuzzing is fun"};
        System.out.println("starting mutation fuzzing...");
        for (int i = 0; i < 1000; i++) {
            // random seed
            String current = seeds[RAND.nextInt(seeds.length)];
            // apply random mutation
            if (RAND.nextBoolean()) {
                current = deleteMutation(current);
            } else {
                current = spaceMutation(current);
            }
            try {
                reverseAndCapWords(current);
            } catch (Exception e) {
                // log mutation-based
                System.out.println("mutation bug found: " + current);
            }
        }
    }
    // mutation op 2: insert random space
    public static String spaceMutation(String s) {
        int index = RAND.nextInt(s.length() + 1);
        return s.substring(0, index) + " " + s.substring(index);
    }
    // professor's test case converted to a simple method
    public static void runOfficialTest() {
        try {
            String input = "this is a test string";
            String expected = "String Test A Is This";
            String actual = reverseAndCapWords(input);
            if (actual.equals(expected)) {
                System.out.println("official test: passed");
            } else {
                System.out.println("official test: failed (expected '" + expected + "' but got '" + actual + "')");
            }
        } catch (Exception e) {
            System.out.println("official test: crashed! " + e.getMessage());
        }
    }
    public static void main(String[] args) {
        // 1. run the basic test first
        runOfficialTest();

        // 2. start fuzzing 100,000 times
        System.out.println("\nstarting fuzzing...");
        int totalIterations = 100000;
        int errorCount = 0;

        for (int i = 1; i <= totalIterations; i++) {
            String testInput = generateRandomInput();
            try {
                reverseAndCapWords(testInput);
            } catch (Exception e) {
                errorCount++;
                // record the first failure for your report 
                if (errorCount == 1) {
                    System.out.println("\n--- first bug found ---");
                    System.out.println("iteration: " + i);
                    System.out.println("input: '" + testInput + "'");
                    System.out.println("error: " + e.toString());
                    System.out.println("-----------------------\n");
                }
            }
        }
        System.out.println("fuzzing done. total bugs found: " + errorCount);
    }
}
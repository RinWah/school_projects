public static String reverseAndCapWords(String input) {
    if (input == null || input.isEmpty()) {
        throw new IllegalArgumentException("Input cannot be null or empty.");
    }
    String[] words = input.split(" ");
    StringBuilder reversedString = new StringBuilder();
    for (int i = words.length - 1; i >= 0; i--) {
        // capitalize the first letter of each string
        String cap = words[i].substring(0,1).toUpperCase() + words[i].subtring(1);
        reversedString.append(cap).append(" ");
    }
    // trim the string to remove the last unnecessary space
    String result = reversedString.toString().trim();
    System.out.println("Reversed words: " + result);
    return result;
}
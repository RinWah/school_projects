import java.util.BitSet;
import org.junit.Test;
import static org.junit.Assert.*;

public class BitSetTest {
    // TR1 (base case): valid positive index within initial size
    @Test
    public void testValidInsideRange() {
        //1. setup: create BitSet with nbits=5
        BitSet b = new BitSet(5);
        //2. action: set bit at index 4
        b.set(4);
        //3. verify: check if get(4) returns true
        assertTrue("Bit 4 should be true after being set", b.get(4));
    }
    // TR2: neg index (the "oops" test)
    @Test(expected = IndexOutOfBoundsException.class)
    public void testNegativeIndex() {
        BitSet b = new BitSet(10);
        b.get(-5); // exception
        }
    // flip state change
    @Test
    public void testFlipChangesValue() {
        BitSet b = new BitSet(10); // all bits are default false
        b.flip(2); // bit 2 is now true
        assertTrue("bit 2 should be true after first flip", b.get(2)); 
        b.flip(2); // bit 2 should be false now
        assertFalse("bit 2 should be false after the second flip", b.get(2));
    }
    // TR3: index outside initial capacity
    @Test
    public void testOutsideInitialCapacity() {
        BitSet b = new BitSet(5); // size is 0-4
        b.set(10); // index 10 > nbits
        assertTrue("BitSet should get bigger to accomodate for index 10", b.get(10));
    }
}
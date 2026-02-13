import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class A1Test {
    @Test
    void baseDiscount_noLoyalty_finalPriceNonNegative() {
        // 1,2,3,5,7 and 7,8,10
        // 1,2,3,5,7,8,10
        int result = A1.calculateDiscount(100,3,false);
        assertEquals(90,result);
    }
    @Test
    void baseDiscount_withLoyalty_finalPriceNonNegative() {
        // 1,2,3,5,6,7 and 7,8,10
        // 1,2,3,5,6,7,8,10
        int result = A1.calculateDiscount(100,6,false);
        assertEquals(85,result);
    }
    @Test
    void specialOffer_noLoyalty_finalPriceNonNegative() {
        // 1,2,4,5,7 and 7,8,10
        // 1,2,4,5,7,8,10
        int result = A1.calculateDiscount(100,3,true);
        assertEquals(80,result);
    }
    @Test
    void specialOffer_withLoyality_finalPriceBecomesZero_whenPriceNegative() {
        // 1,2,4,5,6,7 and 9,10
        // 1,2,4,5,6,7,8,9,10
        int result = A1.calculateDiscount(-100,6,true);
        assertEquals(0,result);
    }
}
/*
infeasible test cases:
we assume that price is greater than 0, obviously not realistic to assume anything less, but we technically cannot check for that.
we also cannot test for finalPrice < 0 and that means nodes 9,10 don't really get tested effectively.
^ both of these are technically testable if you explicitely stated that price < 0 and finalPrice < 0 but feasibly you wouldn't test for that irl.
*/
package payment;

import java.time.Instant;

public record Payment(
        String customerId,
        double amount,
        double usualAmount,
        double amountComparedToUsual,
        String cardType,
        String productType,
        String email,
        String deviceId,
        boolean deviceNew,
        String merchantId,
        boolean merchantNew,
        String merchantType,
        String merchantRisk,
        String location,
        boolean locationChanged,
        Instant time,
        int previousPayments,
        String ip,
        boolean authenticated,
        long secondsSincePrevious,
        String decision
) {
    public Payment withDecision(String decision) {
        return new Payment(
                customerId,
                amount,
                usualAmount,
                amountComparedToUsual,
                cardType,
                productType,
                email,
                deviceId,
                deviceNew,
                merchantId,
                merchantNew,
                merchantType,
                merchantRisk,
                location,
                locationChanged,
                time,
                previousPayments,
                ip,
                authenticated,
                secondsSincePrevious,
                decision
        );
    }
}

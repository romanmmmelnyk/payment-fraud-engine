package payment;

import java.time.Instant;

public record Payment(
        String customerId,
        double amount,
        double usualAmount,
        double amountComparedToUsual,
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
        boolean authenticated
) {
}

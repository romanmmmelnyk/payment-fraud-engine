package payment.fraud;

import payment.Payment;

public class FraudEngine implements FraudCheck {
    public String checkPaymentForFraud(Payment payment) {
        double score = 0;
        if (payment.cardType().equals("credit")) {
            score++;
        }
        if (payment.productType().equals("C")) {
            score++;
        }
        if (!payment.authenticated()) {
            score++;
        }
        score += deviceScore(payment);
        score += merchantScore(payment);
        score += contextScore(payment);

        if (payment.deviceNew() && !payment.authenticated()) {
            return "CHALLENGE";
        }
        if (score < 2) {
            return "APPROVE";
        }
        if (score < 3) {
            return "CHALLENGE";
        }
        return "BLOCK";
    }

    public double deviceScore(Payment payment) {
        // A new device is not a point by itself.
        // Later: ask for 2FA and remember the device as trusted after it passes.
        // Mock: authenticated means 2FA already passed, so the device is trusted.
        // A trusted new device scores 0, or 0.5 when the amount is also high.
        // While 2FA has not passed, checkPaymentForFraud returns CHALLENGE.
        if (!payment.deviceNew() || !payment.authenticated()) {
            return 0;
        }
        if (payment.usualAmount() > 0 && payment.amountComparedToUsual() >= payment.usualAmount()) {
            return 0.5;
        }
        return 0;
    }

    public double contextScore(Payment payment) {
        // Half a point each. Outlook was denser than gmail. Hours 4-9 were denser than the rest of the day.
        // A gap under one hour is the short-burst mock. A normal gap and gmail add nothing.
        double score = 0;
        if (payment.locationChanged()) {
            score += 0.5;
        }
        if (payment.email() != null && payment.email().toLowerCase().contains("outlook")) {
            score += 0.5;
        }
        int hour = payment.time().atZone(java.time.ZoneOffset.UTC).getHour();
        int hour = payment.time().atZone(java.ti)
        if (hour >= 4 && hour <= 9) {
            score += 0.5;
        }
        if (payment.secondsSincePrevious() > 0 && payment.secondsSincePrevious() < 3600) {
            score += 0.5;
        }
        return score;
    }

    public double merchantScore(Payment payment) {
        // Mock of merchant types that normally take large payments.
        // realestate: a house, tens of thousands is normal for the merchant.
        // electronics: a phone or a laptop, high for the customer, normal for the shop.
        // grocery, gas, and the rest do not explain a payment that large.
        //
        // Later, comment only for now:
        // - a merchant new to this customer is not a point by itself;
        
        // - merchantRisk arrives from outside, the system does not check it yet;
        // - if the customer already pays large amounts to this merchant, the amount score should fall to 0;
        // - a high amount that the merchant explains should more often be CHALLENGE, not BLOCK;
        // - a high amount that the merchant does not explain keeps the full point.
        if (!(payment.usualAmount() > 0 && payment.amountComparedToUsual() >= payment.usualAmount())) {
            return 0;
        }
        String merchantType = payment.merchantType();
        if (merchantType.equals("realestate") || merchantType.equals("electronics")) {
            return 0.5;
        }
        return 1;
    }
}

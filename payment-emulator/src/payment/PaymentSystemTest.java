package payment;

import payment.fraud.FraudEngine;

import java.time.Instant;

public class PaymentSystemTest {
    public static void main(String[] args) {
        PaymentSystem system = new PaymentSystem();
        Instant firstTime = Instant.parse("2024-01-01T10:00:00Z");
        Instant secondTime = Instant.parse("2024-01-01T12:00:00Z");

        Payment first = system.pay(
                "customer-1",
                40,
                "credit",
                "C",
                "anna@outlook.com",
                "phone-1",
                "shop-1",
                "grocery",
                "low",
                "Kyiv",
                firstTime,
                "10.0.0.1",
                true
        );
        check(first.usualAmount() == 0, "first payment has no usual amount");
        check(first.amountComparedToUsual() == 0, "first payment is not compared");
        check(first.deviceNew(), "first device is new");
        check(first.merchantNew(), "first merchant is new");
        check(!first.locationChanged(), "first location is not a change");
        check(first.previousPayments() == 0, "first payment has no history");
        check(first.authenticated(), "authentication is stored");
        check("10.0.0.1".equals(first.ip()), "ip is stored");
        check("credit".equals(first.cardType()), "card type is stored");
        check("C".equals(first.productType()), "product type is stored");
        check("anna@outlook.com".equals(first.email()), "email is stored");
        check("CHALLENGE".equals(first.decision()), "first payment is challenged");

        Payment second = system.pay(
                "customer-1",
                70,
                "debit",
                "W",
                "anna@gmail.com",
                "phone-1",
                "shop-2",
                "travel",
                "high",
                "Lviv",
                secondTime,
                "10.0.0.2",
                false
        );
        check(second.usualAmount() == 40, "usual amount is the previous average");
        check(second.amountComparedToUsual() == 30, "amount is compared with the usual amount");
        check(!second.deviceNew(), "same device is not new");
        check(second.merchantNew(), "new merchant is new");
        check(second.locationChanged(), "location change is stored");
        check(second.previousPayments() == 1, "one previous payment is counted");
        check(second.secondsSincePrevious() == 7200, "gap since the previous payment is two hours");
        check("high".equals(second.merchantRisk()), "merchant risk is stored");
        check(!second.authenticated(), "missing authentication is stored");
        check("debit".equals(second.cardType()), "second card type is stored");
        check("W".equals(second.productType()), "second product type is stored");
        check("anna@gmail.com".equals(second.email()), "second email is stored");
        check("APPROVE".equals(second.decision()), "second payment is approved");

        check(system.history("customer-1").size() == 2, "history keeps both payments");
        check(system.history("customer-2").isEmpty(), "another customer starts empty");

        Payment other = system.pay(
                "customer-2",
                15,
                "credit",
                "C",
                "other@gmail.com",
                "phone-1",
                "shop-1",
                "grocery",
                "low",
                "Kyiv",
                secondTime,
                "10.0.0.3",
                true
        );
        check(other.deviceNew(), "device is new for a new customer");
        check(other.merchantNew(), "merchant is new for a new customer");
        check(system.history("customer-1").size() == 2, "other customer does not change the first history");

        FraudEngine engine = new FraudEngine();
        Payment house = new Payment(
                "customer-3",
                200000,
                40,
                199960,
                "debit",
                "W",
                "anna@gmail.com",
                "phone-1",
                false,
                "estate-1",
                true,
                "realestate",
                "low",
                "Kyiv",
                false,
                secondTime,
                1,
                "10.0.0.1",
                true,
                0,
                null
        );
        Payment phone = new Payment(
                "customer-3",
                800,
                40,
                760,
                "debit",
                "W",
                "anna@gmail.com",
                "phone-1",
                false,
                "shop-3",
                true,
                "electronics",
                "low",
                "Kyiv",
                false,
                secondTime,
                1,
                "10.0.0.1",
                true,
                0,
                null
        );
        Payment groceries = new Payment(
                "customer-3",
                800,
                40,
                760,
                "debit",
                "W",
                "anna@gmail.com",
                "phone-1",
                false,
                "shop-1",
                false,
                "grocery",
                "low",
                "Kyiv",
                false,
                secondTime,
                1,
                "10.0.0.1",
                true,
                0,
                null
        );
        check(engine.merchantScore(house) == 0.5, "realestate explains a high amount");
        check(engine.merchantScore(phone) == 0.5, "electronics explains a high amount");
        check(engine.merchantScore(groceries) == 1, "grocery does not explain a high amount");

        System.out.println("ok");
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}

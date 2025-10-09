package com.gos.lib.properties.feedforward;

import com.gos.lib.properties.BasePropertiesTest;
import edu.wpi.first.wpilibj.Preferences;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ArmFeedForwardPropertyTest extends BasePropertiesTest {
    private static final String PROPERTY_NAME = "ArmFeedForwardTest";

    @Test
    public void testParameterSetting() {
        ArmFeedForwardProperty property = new ArmFeedForwardProperty(PROPERTY_NAME, false)
            .addKff(1)
            .addKs(2)
            .addKa(3)
            .addKg(4);

        // Check initial setup
        assertEquals(1, property.getKFf());
        assertEquals(2, property.getKs());
        assertEquals(3, property.getKa());
        assertEquals(4, property.getKg());
        assertEquals(4 + 1, Preferences.getKeys().size());

        // Change the values, but do not update the properties. Should remain the same as the defaults
        Preferences.setDouble(PROPERTY_NAME + ".aff.kff", 1.5);
        Preferences.setDouble(PROPERTY_NAME + ".aff.ks", 0.5);
        Preferences.setDouble(PROPERTY_NAME + ".aff.ka", 2);
        Preferences.setDouble(PROPERTY_NAME + ".aff.kg", 1);
        assertEquals(1, property.getKFf());
        assertEquals(2, property.getKs());
        assertEquals(3, property.getKa());
        assertEquals(4, property.getKg());
        assertEquals(4 + 1, Preferences.getKeys().size());

        // Update the properties and assert they have changed
        property.updateIfChanged();
        assertEquals(1.5, property.getKFf());
        assertEquals(0.5, property.getKs());
        assertEquals(2, property.getKa());
        assertEquals(1, property.getKg());
        assertEquals(4 + 1, Preferences.getKeys().size());
    }
}

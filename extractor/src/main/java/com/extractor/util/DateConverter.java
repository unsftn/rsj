package com.extractor.util;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.TimeZone;

public class DateConverter {

    public static String convertDateToISO8601(Date date) {
        if (date == null) {
            return null;
        }

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSXXX");
        sdf.setTimeZone(TimeZone.getTimeZone("CET"));
        return sdf.format(date);
    }

    public static String convertCalendarToISO8601(Calendar calendar) {
        if (calendar == null) {
            return null;
        }

        return convertDateToISO8601(calendar.getTime());
    }
}

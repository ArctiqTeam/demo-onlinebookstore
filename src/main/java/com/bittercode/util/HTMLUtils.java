package com.bittercode.util;

import org.apache.commons.text.StringEscapeUtils;

public class HTMLUtils {

    public static String escapeHtml(String input) {
        return StringEscapeUtils.escapeHtml4(input);
    }
}
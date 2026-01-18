package com.lwyr.ai

import org.springframework.boot.SpringApplication
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.ConfigurationPropertiesScan

@SpringBootApplication
@ConfigurationPropertiesScan
class LwyrApplication

fun main(args: Array<String>) {
    SpringApplication.run(LwyrApplication::class.java, *args)
}

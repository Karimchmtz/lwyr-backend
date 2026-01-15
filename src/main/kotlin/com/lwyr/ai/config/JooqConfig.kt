package com.lwyr.ai.config

import org.jooq.DSLContext
import org.jooq.SQLDialect
import org.jooq.impl.DefaultDSLContext
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import javax.sql.DataSource

@Configuration
class DatabaseConfig {

    @Bean
    fun dslContext(dataSource: DataSource): DSLContext {
        return DefaultDSLContext(dataSource, SQLDialect.POSTGRES)
    }
}

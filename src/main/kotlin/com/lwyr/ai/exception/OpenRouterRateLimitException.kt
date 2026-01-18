package com.lwyr.ai.exception

import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.ResponseStatus

@ResponseStatus(HttpStatus.TOO_MANY_REQUESTS)
class OpenRouterRateLimitException(message: String) : OpenRouterException(message)

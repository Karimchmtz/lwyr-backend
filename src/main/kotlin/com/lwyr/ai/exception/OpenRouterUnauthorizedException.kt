package com.lwyr.ai.exception

import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.ResponseStatus

@ResponseStatus(HttpStatus.UNAUTHORIZED)
class OpenRouterUnauthorizedException(message: String) : OpenRouterException(message)

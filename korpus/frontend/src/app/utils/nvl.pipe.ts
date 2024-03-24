import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'nvl'})
export class NvlPipe implements PipeTransform {

  transform(value: string, replacement: string): string {
    if (!value)
      return replacement;
    return value;
  }

}